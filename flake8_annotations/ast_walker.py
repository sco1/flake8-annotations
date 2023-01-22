from __future__ import annotations

import ast
import typing as t

from attrs import define

from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType

AST_DECORATOR_NODES = t.Union[ast.Attribute, ast.Call, ast.Name]
AST_DEF_NODES = t.Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
AST_FUNCTION_TYPES = t.Union[ast.FunctionDef, ast.AsyncFunctionDef]

# The order of AST_ARG_TYPES must match Python's grammar
# See: https://docs.python.org/3/library/ast.html#abstract-grammar
AST_ARG_TYPES: t.Tuple[str, ...] = ("posonlyargs", "args", "vararg", "kwonlyargs", "kwarg")


@define(slots=True)
class Argument:
    """Represent a function argument & its metadata."""

    argname: str
    lineno: int
    col_offset: int
    annotation_type: AnnotationType
    has_type_annotation: bool = False
    has_type_comment: bool = False
    is_dynamically_typed: bool = False

    def __str__(self) -> str:
        """
        Format the Argument object into a readable representation.

        The output string will be formatted as:
          '<Argument: <argname>, Annotated: <has_type_annotation>>'
        """
        return f"<Argument: {self.argname}, Annotated: {self.has_type_annotation}>"

    @classmethod
    def from_arg_node(cls, node: ast.arg, annotation_type_name: str) -> Argument:
        """Create an Argument object from an ast.arguments node."""
        annotation_type = AnnotationType[annotation_type_name]
        new_arg = cls(node.arg, node.lineno, node.col_offset, annotation_type)

        if node.annotation:
            new_arg.has_type_annotation = True

            if cls._is_annotated_any(node.annotation):
                new_arg.is_dynamically_typed = True

        if node.type_comment:
            new_arg.has_type_comment = True

        return new_arg

    @staticmethod
    def _is_annotated_any(arg_expr: ast.expr) -> bool:
        """
        Check if the provided expression node is annotated with `typing.Any`.

        Support is provided for the following patterns:
            * `from typing import Any; foo: Any`
            * `import typing; foo: typing.Any`
            * `import typing as <alias>; foo: <alias>.Any`
        """
        if isinstance(arg_expr, ast.Name):
            if arg_expr.id == "Any":
                return True
        elif isinstance(arg_expr, ast.Attribute):
            if arg_expr.attr == "Any":
                return True

        return False


@define(slots=True)
class Function:
    """
    Represent a function and its relevant metadata.

    Note: while Python differentiates between a function and a method, for the purposes of this
    tool, both will be referred to as functions outside of any class-specific context. This also
    aligns with ast's naming convention.
    """

    name: str
    lineno: int
    col_offset: int
    decorator_list: t.List[AST_DECORATOR_NODES]
    args: t.List[Argument]
    function_type: FunctionType = FunctionType.PUBLIC
    is_class_method: bool = False
    class_decorator_type: t.Union[ClassDecoratorType, None] = None
    is_return_annotated: bool = False
    has_type_comment: bool = False
    has_only_none_returns: bool = True
    is_nested: bool = False

    def is_fully_annotated(self) -> bool:
        """
        Check that all of the function's inputs are type annotated.

        Note that self.args will always include an Argument object for return
        """
        return all(arg.has_type_annotation for arg in self.args)

    def is_dynamically_typed(self) -> bool:
        """Determine if the function is dynamically typed, defined as completely lacking hints."""
        return not any(arg.has_type_annotation for arg in self.args)

    def get_missed_annotations(self) -> t.List[Argument]:
        """Provide a list of arguments with missing type annotations."""
        return [arg for arg in self.args if not arg.has_type_annotation]

    def get_annotated_arguments(self) -> t.List[Argument]:
        """Provide a list of arguments with type annotations."""
        return [arg for arg in self.args if arg.has_type_annotation]

    def has_decorator(self, check_decorators: t.Set[str]) -> bool:
        """
        Determine whether the function node is decorated by any of the provided decorators.

        Decorator matching is done against the provided `check_decorators` set, allowing the user
        to specify any expected aliasing in the relevant flake8 configuration option. Decorators are
        assumed to be either a module attribute (e.g. `@typing.overload`) or name
        (e.g. `@overload`). For the case of a module attribute, only the attribute is checked
        against `overload_decorators`.

        NOTE: Deeper decorator imports (e.g. `a.b.overload`) are not explicitly supported
        """
        for decorator in self.decorator_list:
            # Drop to a helper to allow for simpler handling of callable decorators
            return self._decorator_checker(decorator, check_decorators)
        else:
            return False

    def _decorator_checker(
        self, decorator: AST_DECORATOR_NODES, check_decorators: t.Set[str]
    ) -> bool:
        """
        Check the provided decorator for a match against the provided set of check names.

        Decorators are assumed to be of the following form:
            * `a.name` or `a.name()`
            * `name` or `name()`

        NOTE: Deeper imports (e.g. `a.b.name`) are not explicitly supported.
        """
        if isinstance(decorator, ast.Name):
            # e.g. `@overload`, where `decorator.id` will be the name
            if decorator.id in check_decorators:
                return True
        elif isinstance(decorator, ast.Attribute):
            # e.g. `@typing.overload`, where `decorator.attr` will be the name
            if decorator.attr in check_decorators:
                return True
        elif isinstance(decorator, ast.Call):  # pragma: no branch
            # e.g. `@overload()` or `@typing.overload()`, where `decorator.func` will be `ast.Name`
            # or `ast.Attribute`, which we can check recursively
            # Ignore typing here, the AST stub just uses `expr` as the type for `decorator.func`
            return self._decorator_checker(decorator.func, check_decorators)  # type: ignore[arg-type]  # noqa: E501

        # There shouldn't be any possible way to get here
        return False  # pragma: no cover

    def __str__(self) -> str:
        """
        Format the Function object into a readable representation.

        The output string will be formatted as:
          '<Function: <name>, Args: <args>>'
        """
        # Manually join the list so we get Argument's __str__ instead of __repr__
        # Function will always have a list of at least one Argument ("return" is always added)
        str_args = f"[{', '.join([str(arg) for arg in self.args])}]"

        return f"<Function: {self.name}, Args: {str_args}>"

    @classmethod
    def from_function_node(
        cls, node: AST_FUNCTION_TYPES, lines: t.List[str], **kwargs: t.Any
    ) -> Function:
        """
        Create an Function object from ast.FunctionDef or ast.AsyncFunctionDef nodes.

        Accept the source code, as a list of strings, in order to get the column where the function
        definition ends.

        With exceptions, input kwargs are passed straight through to Function's __init__. The
        following kwargs will be overridden:
          * function_type
          * class_decorator_type
          * args
        """
        # Extract function types from function name
        kwargs["function_type"] = cls.get_function_type(node.name)

        # Identify type of class method, if applicable
        if kwargs.get("is_class_method", False):
            kwargs["class_decorator_type"] = cls.get_class_decorator_type(node)

        # Store raw decorator list for use by property methods
        kwargs["decorator_list"] = node.decorator_list

        # Instantiate empty args list here since it has no default (mutable defaults bad!)
        kwargs["args"] = []

        new_function = cls(node.name, node.lineno, node.col_offset, **kwargs)

        # Iterate over arguments by type & add
        for arg_type in AST_ARG_TYPES:
            args = node.args.__getattribute__(arg_type)
            if args:
                if not isinstance(args, list):
                    args = [args]

                new_function.args.extend(
                    [Argument.from_arg_node(arg, arg_type.upper()) for arg in args]
                )

        # Create an Argument object for the return hint
        def_end_lineno, def_end_col_offset = cls.colon_seeker(node, lines)
        return_arg = Argument("return", def_end_lineno, def_end_col_offset, AnnotationType.RETURN)
        if node.returns:
            return_arg.has_type_annotation = True
            new_function.is_return_annotated = True

            if Argument._is_annotated_any(node.returns):
                return_arg.is_dynamically_typed = True

        new_function.args.append(return_arg)

        if node.type_comment:
            new_function.has_type_comment = True

        # Check for the presence of non-`None` returns using the special-case return node visitor
        return_visitor = ReturnVisitor(node)
        return_visitor.visit(node)
        new_function.has_only_none_returns = return_visitor.has_only_none_returns

        return new_function

    @staticmethod
    def colon_seeker(node: AST_FUNCTION_TYPES, lines: t.List[str]) -> t.Tuple[int, int]:
        """
        Find the line & column indices of the function definition's closing colon.

        For Python >= 3.8, docstrings are contained in the body of the function node.

        NOTE: AST's line numbers are 1-indexed, column offsets are 0-indexed. Since `lines` is a
        list, it will be 0-indexed.
        """
        # Special case single line function definitions
        if node.lineno == node.body[0].lineno:
            return Function._single_line_colon_seeker(node, lines[node.lineno - 1])

        # Once we've gotten here, we've found the line where the docstring begins, so we have
        # to step up one more line to get to the close of the def
        def_end_lineno = node.body[0].lineno
        def_end_lineno -= 1

        # Use str.rfind() to account for annotations on the same line, definition closure should
        # be the last : on the line
        def_end_col_offset = lines[def_end_lineno - 1].rfind(":")

        return def_end_lineno, def_end_col_offset

    @staticmethod
    def _single_line_colon_seeker(node: AST_FUNCTION_TYPES, line: str) -> t.Tuple[int, int]:
        """Locate the closing colon for a single-line function definition."""
        col_start = node.col_offset
        col_end = node.body[0].col_offset
        def_end_col_offset = line.rfind(":", col_start, col_end)

        return node.lineno, def_end_col_offset

    @staticmethod
    def get_function_type(function_name: str) -> FunctionType:
        """
        Determine the function's FunctionType from its name.

        MethodType is determined by the following priority:
          1. Special: function name prefixed & suffixed by "__"
          2. Private: function name prefixed by "__"
          3. Protected: function name prefixed by "_"
          4. Public: everything else
        """
        if function_name.startswith("__") and function_name.endswith("__"):
            return FunctionType.SPECIAL
        elif function_name.startswith("__"):
            return FunctionType.PRIVATE
        elif function_name.startswith("_"):
            return FunctionType.PROTECTED
        else:
            return FunctionType.PUBLIC

    @staticmethod
    def get_class_decorator_type(
        function_node: AST_FUNCTION_TYPES,
    ) -> t.Union[ClassDecoratorType, None]:
        """
        Get the class method's decorator type from its function node.

        For the purposes of this tool, only @classmethod and @staticmethod decorators are
        identified; all other decorators are ignored

        If @classmethod or @staticmethod decorators are not present, this function will return None
        """
        # @classmethod and @staticmethod will show up as ast.Name objects, where callable decorators
        # will show up as ast.Call, which we can ignore
        decorators = [
            decorator.id
            for decorator in function_node.decorator_list
            if isinstance(decorator, ast.Name)
        ]

        if "classmethod" in decorators:
            return ClassDecoratorType.CLASSMETHOD
        elif "staticmethod" in decorators:
            return ClassDecoratorType.STATICMETHOD
        else:
            return None


class FunctionVisitor(ast.NodeVisitor):
    """An ast.NodeVisitor instance for walking the AST and describing all contained functions."""

    AST_FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)

    def __init__(self, lines: t.List[str]):
        self.lines = lines
        self.function_definitions: t.List[Function] = []
        self._context: t.List[AST_DEF_NODES] = []

    def switch_context(self, node: AST_DEF_NODES) -> None:
        """
        Utilize a context switcher as a generic function visitor in order to track function context.

        Without keeping track of context, it's challenging to reliably differentiate class methods
        from "regular" functions, especially in the case of nested classes.

        Thank you for the inspiration @isidentical :)
        """
        if isinstance(node, self.AST_FUNC_TYPES):
            # Check for non-empty context first to prevent IndexErrors for non-nested nodes
            if self._context:
                if isinstance(self._context[-1], ast.ClassDef):
                    # Check if current context is a ClassDef node & pass the appropriate flag
                    self.function_definitions.append(
                        Function.from_function_node(node, self.lines, is_class_method=True)
                    )
                elif isinstance(self._context[-1], self.AST_FUNC_TYPES):  # pragma: no branch
                    # Check for nested function & pass the appropriate flag
                    self.function_definitions.append(
                        Function.from_function_node(node, self.lines, is_nested=True)
                    )
            else:
                self.function_definitions.append(Function.from_function_node(node, self.lines))

        self._context.append(node)
        self.generic_visit(node)
        self._context.pop()

    visit_FunctionDef = switch_context
    visit_AsyncFunctionDef = switch_context
    visit_ClassDef = switch_context


class ReturnVisitor(ast.NodeVisitor):
    """
    Special-case of `ast.NodeVisitor` for visiting return statements of a function node.

    If the function node being visited has an explicit return statement of anything other than
    `None`, the `instance.has_only_none_returns` flag will be set to `False`.

    If the function node being visited has no return statement, or contains only return
    statement(s) that explicitly return `None`, the `instance.has_only_none_returns` flag will be
    set to `True`.

    Due to the generic visiting being done, we need to keep track of the context in which a
    non-`None` return node is found. These functions are added to a set that is checked to see
    whether nor not the parent node is present.
    """

    def __init__(self, parent_node: AST_FUNCTION_TYPES):
        self.parent_node = parent_node
        self._context: t.List[AST_FUNCTION_TYPES] = []
        self._non_none_return_nodes: t.Set[AST_FUNCTION_TYPES] = set()

    @property
    def has_only_none_returns(self) -> bool:
        """Return `True` if the parent node isn't in the visited nodes that don't return `None`."""
        return self.parent_node not in self._non_none_return_nodes

    def visit_Return(self, node: ast.Return) -> None:
        """
        Check each Return node to see if it returns anything other than `None`.

        If the node being visited returns anything other than `None`, its parent context is added to
        the set of non-returning child nodes of the parent node.
        """
        if node.value is not None:
            # In the event of an explicit `None` return (`return None`), the node body will be an
            # instance of either `ast.Constant` (3.8+) or `ast.NameConstant`, which we need to check
            # to see if it's actually `None`
            if isinstance(node.value, (ast.Constant, ast.NameConstant)):  # pragma: no branch
                if node.value.value is None:
                    return

            self._non_none_return_nodes.add(self._context[-1])

    def switch_context(self, node: AST_FUNCTION_TYPES) -> None:
        """
        Utilize a context switcher as a generic visitor in order to properly track function context.

        Using a traditional `ast.generic_visit` setup, return nodes of nested functions are visited
        without any knowledge of their context, causing the top-level function to potentially be
        mis-classified.

        Thank you for the inspiration @isidentical :)
        """
        self._context.append(node)
        self.generic_visit(node)
        self._context.pop()

    visit_FunctionDef = switch_context
    visit_AsyncFunctionDef = switch_context
