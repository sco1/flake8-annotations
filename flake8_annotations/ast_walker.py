from __future__ import annotations

import typing as t
from itertools import zip_longest

from attrs import define

from flake8_annotations import PY_GTE_38
from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType

# Check if we can use the stdlib ast module instead of typed_ast; stdlib ast gains native type
# comment support in Python 3.8
if PY_GTE_38:
    import ast
    from ast import Ellipsis as ast_Ellipsis
else:
    from typed_ast import ast3 as ast  # type: ignore[no-redef]
    from typed_ast.ast3 import Ellipsis as ast_Ellipsis  # type: ignore[misc]


AST_DECORATOR_NODES = t.Union[ast.Attribute, ast.Call, ast.Name]
AST_DEF_NODES = t.Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
AST_FUNCTION_TYPES = t.Union[ast.FunctionDef, ast.AsyncFunctionDef]

# The order of AST_ARG_TYPES must match Python's grammar
# See: https://docs.python.org/3/library/ast.html#abstract-grammar
AST_ARG_TYPES: t.Tuple[str, ...] = ("args", "vararg", "kwonlyargs", "kwarg")
if PY_GTE_38:
    # Positional-only args introduced in Python 3.8
    # If posonlyargs are present, they will be before other argument types
    AST_ARG_TYPES = ("posonlyargs",) + AST_ARG_TYPES


@define(slots=True)
class Argument:
    """Represent a function argument & its metadata."""

    argname: str
    lineno: int
    col_offset: int
    annotation_type: AnnotationType
    has_type_annotation: bool = False
    has_3107_annotation: bool = False
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

        new_arg.has_type_annotation = False
        if node.annotation:
            new_arg.has_type_annotation = True
            new_arg.has_3107_annotation = True

            if cls._is_annotated_any(node.annotation):
                new_arg.is_dynamically_typed = True

        if node.type_comment:
            new_arg.has_type_annotation = True
            new_arg.has_type_comment = True

            if cls._is_annotated_any(node.type_comment):
                new_arg.is_dynamically_typed = True

        return new_arg

    @staticmethod
    def _is_annotated_any(arg_expr: t.Union[ast.expr, str]) -> bool:
        """
        Check if the provided expression node is annotated with `typing.Any`.

        Support is provided for the following patterns:
            * `from typing import Any; foo: Any`
            * `import typing; foo: typing.Any`
            * `import typing as <alias>; foo: <alias>.Any`

        Type comments are also supported. Inline type comments are assumed to be passed here as
        `str`, and function-level type comments are assumed to be passed as `ast.expr`.
        """
        if isinstance(arg_expr, ast.Name):
            if arg_expr.id == "Any":
                return True
        elif isinstance(arg_expr, ast.Attribute):
            if arg_expr.attr == "Any":
                return True
        elif isinstance(arg_expr, str):
            if arg_expr.split(".", maxsplit=1)[-1] == "Any":
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
            return_arg.has_3107_annotation = True
            new_function.is_return_annotated = True

            if Argument._is_annotated_any(node.returns):
                return_arg.is_dynamically_typed = True

        new_function.args.append(return_arg)

        # Type comments in-line with input arguments are handled by the Argument class
        # If a function-level type comment is present, attempt to parse for any missed type hints
        if node.type_comment:
            new_function.has_type_comment = True
            new_function = cls.try_type_comment(new_function, node)

        # Check for the presence of non-`None` returns using the special-case return node visitor
        return_visitor = ReturnVisitor(node)
        return_visitor.visit(node)
        new_function.has_only_none_returns = return_visitor.has_only_none_returns

        return new_function

    @staticmethod
    def colon_seeker(node: AST_FUNCTION_TYPES, lines: t.List[str]) -> t.Tuple[int, int]:
        """
        Find the line & column indices of the function definition's closing colon.

        Processing paths are Python version-dependent, as there are differences in where the
        docstring is placed in the AST:
            * Python >= 3.8, docstrings are contained in the body of the function node
            * Python < 3.8, docstrings are contained in the function node

        NOTE: AST's line numbers are 1-indexed, column offsets are 0-indexed. Since `lines` is a
        list, it will be 0-indexed.
        """
        # Special case single line function definitions
        if node.lineno == node.body[0].lineno:
            return Function._single_line_colon_seeker(node, lines[node.lineno - 1])

        # With Python < 3.8, the function node includes the docstring & the body does not, so
        # we have rewind through any docstrings, if present, before looking for the def colon
        # We should end up with lines[def_end_lineno - 1] having the colon
        def_end_lineno = node.body[0].lineno
        if not PY_GTE_38:
            # If the docstring is on one line then no rewinding is necessary.
            n_triple_quotes = lines[def_end_lineno - 1].count('"""')
            if n_triple_quotes == 1:  # pragma: no branch
                # Docstring closure, rewind until the opening is found & take the line prior
                while True:
                    def_end_lineno -= 1
                    if '"""' in lines[def_end_lineno - 1]:  # pragma: no branch
                        # Docstring has closed
                        break

        # Once we've gotten here, we've found the line where the docstring begins, so we have
        # to step up one more line to get to the close of the def
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
    def try_type_comment(func_obj: Function, node: AST_FUNCTION_TYPES) -> Function:
        """
        Attempt to infer type hints from a function-level type comment.

        If a function is type commented it is assumed to have a return annotation, otherwise Python
        will fail to parse the hint.
        """
        # If we're in this function then the node is guaranteed to have a type comment, so we can
        # ignore mypy's complaint about an incompatible type for `node.type_comment`
        # Because we're passing in the `func_type` arg, we know that our return is guaranteed to be
        # ast.FunctionType
        hint_tree: ast.FunctionType = ast.parse(node.type_comment, "<func_type>", "func_type")  # type: ignore[assignment, arg-type]  # noqa: E501
        hint_tree = Function._maybe_inject_class_argument(hint_tree, func_obj)

        for arg, hint_comment in zip_longest(func_obj.args, hint_tree.argtypes):
            if isinstance(hint_comment, ast_Ellipsis):
                continue

            if arg and hint_comment:
                arg.has_type_annotation = True
                arg.has_type_comment = True

                if Argument._is_annotated_any(hint_comment):
                    arg.is_dynamically_typed = True

        # Return arg is always last
        func_obj.args[-1].has_type_annotation = True
        func_obj.args[-1].has_type_comment = True
        func_obj.is_return_annotated = True
        if Argument._is_annotated_any(hint_tree.returns):
            arg.is_dynamically_typed = True

        return func_obj

    @staticmethod
    def _maybe_inject_class_argument(
        hint_tree: ast.FunctionType, func_obj: Function
    ) -> ast.FunctionType:
        """
        Inject `self` or `cls` args into a type comment to align with PEP 3107-style annotations.

        Because PEP 484 does not describe a method to provide partial function-level type comments,
        there is a potential for ambiguity in the context of both class methods and classmethods
        when aligning type comments to method arguments.

        These two class methods, for example, should lint equivalently:

            def bar(self, a):
                # type: (int) -> int
                ...

            def bar(self, a: int) -> int
                ...

        When this example type comment is parsed by `ast` and then matched with the method's
        arguments, it associates the `int` hint to `self` rather than `a`, so a dummy hint needs to
        be provided in situations where `self` or `class` are not hinted in the type comment in
        order to achieve equivalent linting results to PEP-3107 style annotations.

        A dummy `ast.Ellipses` constant is injected if the following criteria are met:
            1. The function node is either a class method or classmethod
            2. The number of hinted args is at least 1 less than the number of function args
        """
        if not func_obj.is_class_method:
            # Short circuit
            return hint_tree

        if func_obj.class_decorator_type != ClassDecoratorType.STATICMETHOD:
            if len(hint_tree.argtypes) < (len(func_obj.args) - 1):  # Subtract 1 to skip return arg
                # Ignore mypy's objection to this assignment, Ellipsis subclasses expr so I'm not
                # sure how to make Mypy happy with this but I think it still makes semantic sense
                hint_tree.argtypes = [ast.Ellipsis()] + hint_tree.argtypes  # type: ignore[assignment, operator]  # noqa: E501

        return hint_tree

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
