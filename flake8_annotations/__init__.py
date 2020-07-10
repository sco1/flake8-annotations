import sys
from itertools import zip_longest
from typing import List, Set, Tuple, Union

from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType

# Check if we can use the stdlib ast module instead of typed_ast
# stdlib ast gains native type comment support in Python 3.8
if sys.version_info >= (3, 8):
    import ast
    from ast import Ellipsis as ast_Ellipsis

    PY_GTE_38 = True
else:
    from typed_ast import ast3 as ast
    from typed_ast.ast3 import Ellipsis as ast_Ellipsis

    PY_GTE_38 = False

__version__ = "2.2.1"

AST_ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")
if PY_GTE_38:
    # Positional-only args introduced in Python 3.8
    AST_ARG_TYPES += ("posonlyargs",)

AST_FUNCTION_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef]
AST_DEF_NODES = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]


class Argument:
    """Represent a function argument & its metadata."""

    def __init__(
        self,
        argname: str,
        lineno: int,
        col_offset: int,
        annotation_type: AnnotationType,
        has_type_annotation: bool = False,
        has_3107_annotation: bool = False,
        has_type_comment: bool = False,
    ):
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
        self.annotation_type = annotation_type
        self.has_type_annotation = has_type_annotation
        self.has_3107_annotation = has_3107_annotation
        self.has_type_comment = has_type_comment

    def __str__(self) -> str:
        """
        Format the Argument object into a readable representation.

        The output string will be formatted as:
          '<Argument: <argname>, Annotated: <has_type_annotation>>'
        """
        return f"<Argument: {self.argname}, Annotated: {self.has_type_annotation}>"

    def __repr__(self) -> str:
        """Format the Argument object into its "official" representation."""
        return (
            f"Argument("
            f"argname={self.argname!r}, "
            f"lineno={self.lineno}, "
            f"col_offset={self.col_offset}, "
            f"annotation_type={self.annotation_type}, "
            f"has_type_annotation={self.has_type_annotation}, "
            f"has_3107_annotation={self.has_3107_annotation}, "
            f"has_type_comment={self.has_type_comment}"
            ")"
        )

    @classmethod
    def from_arg_node(cls, node: ast.arguments, annotation_type_name: str):
        """Create an Argument object from an ast.arguments node."""
        annotation_type = AnnotationType[annotation_type_name]
        new_arg = cls(node.arg, node.lineno, node.col_offset, annotation_type)

        new_arg.has_type_annotation = False
        if node.annotation:
            new_arg.has_type_annotation = True
            new_arg.has_3107_annotation = True

        if node.type_comment:
            new_arg.has_type_annotation = True
            new_arg.has_type_comment = True

        return new_arg


class Function:
    """
    Represent a function and its relevant metadata.

    Note: while Python differentiates between a function and a method, for the purposes of this
    tool, both will be referred to as functions outside of any class-specific context. This also
    aligns with ast's naming convention.
    """

    def __init__(
        self,
        name: str,
        lineno: int,
        col_offset: int,
        function_type: FunctionType = FunctionType.PUBLIC,
        is_class_method: bool = False,
        class_decorator_type: Union[ClassDecoratorType, None] = None,
        is_return_annotated: bool = False,
        has_type_comment: bool = False,
        has_only_none_returns: bool = True,
        args: List[Argument] = None,
    ):
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.function_type = function_type
        self.is_class_method = is_class_method
        self.class_decorator_type = class_decorator_type
        self.is_return_annotated = is_return_annotated
        self.has_type_comment = has_type_comment
        self.has_only_none_returns = has_only_none_returns
        self.args = args

    def is_fully_annotated(self) -> bool:
        """
        Check that all of the function's inputs are type annotated.

        Note that self.args will always include an Argument object for return
        """
        return all(arg.has_type_annotation for arg in self.args)

    def is_dynamically_typed(self) -> bool:
        """Determine if the function is dynamically typed, defined as completely lacking hints."""
        return not any(arg.has_type_annotation for arg in self.args)

    def get_missed_annotations(self) -> List:
        """Provide a list of arguments with missing type annotations."""
        return [arg for arg in self.args if not arg.has_type_annotation]

    def get_annotated_arguments(self) -> List:
        """Provide a list of arguments with type annotations."""
        return [arg for arg in self.args if arg.has_type_annotation]

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

    def __repr__(self) -> str:
        """Format the Function object into its "official" representation."""
        return (
            f"Function("
            f"name={self.name!r}, "
            f"lineno={self.lineno}, "
            f"col_offset={self.col_offset}, "
            f"function_type={self.function_type}, "
            f"is_class_method={self.is_class_method}, "
            f"class_decorator_type={self.class_decorator_type}, "
            f"is_return_annotated={self.is_return_annotated}, "
            f"has_type_comment={self.has_type_comment}, "
            f"has_only_none_returns={self.has_only_none_returns}, "
            f"args={self.args}"
            ")"
        )

    @classmethod
    def from_function_node(cls, node: AST_FUNCTION_TYPES, lines: List[str], **kwargs):
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
        if kwargs.get("is_class_method", False):
            kwargs["class_decorator_type"] = cls.get_class_decorator_type(node)

        new_function = cls(node.name, node.lineno, node.col_offset, **kwargs)

        # Iterate over arguments by type & add
        new_function.args = []
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
    def colon_seeker(node: AST_FUNCTION_TYPES, lines: List[str]) -> Tuple[int, int]:
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

        def_end_lineno = node.body[0].lineno - 1

        # With Python < 3.8, the function node includes the docstring & the body does not, so
        # we have rewind through any docstrings, if present, before looking for the def colon
        if not PY_GTE_38:
            # This list index is a little funky, since we've already subtracted 1 outside of this
            # context, we can leave it as-is since it will index the list to the line prior to where
            # the function node's body begins.
            # If the docstring is on one line then no rewinding is necessary.
            n_triple_quotes = lines[def_end_lineno].count('"""')
            if n_triple_quotes == 1:
                # Docstring closure, rewind until the opening is found & take the line prior
                while True:
                    def_end_lineno -= 1
                    if '"""' in lines[def_end_lineno - 1]:
                        # Docstring has closed
                        def_end_lineno -= 1
                        break

        # Use str.rfind() to account for annotations on the same line, definition closure should
        # be the last : on the line
        def_end_col_offset = lines[def_end_lineno - 1].rfind(":") + 1

        return def_end_lineno, def_end_col_offset

    @staticmethod
    def _single_line_colon_seeker(node: AST_FUNCTION_TYPES, line: str) -> Tuple[int, int]:
        """Locate the closing colon for a single-line function definition."""
        col_start = node.col_offset
        col_end = node.body[0].col_offset
        def_end_col_offset = line.rfind(":", col_start, col_end) + 1

        return node.lineno, def_end_col_offset

    @staticmethod
    def try_type_comment(func_obj: "Function", node: AST_FUNCTION_TYPES) -> "Function":
        """
        Attempt to infer type hints from a function-level type comment.

        If a function is type commented it is assumed to have a return annotation, otherwise Python
        will fail to parse the hint
        """
        hint_tree = ast.parse(node.type_comment, "<func_type>", "func_type")

        for arg, hint_comment in zip_longest(func_obj.args, hint_tree.argtypes):
            if isinstance(hint_comment, ast_Ellipsis):
                continue

            if arg and hint_comment:
                arg.has_type_annotation = True
                arg.has_type_comment = True

        # Return arg is always last
        func_obj.args[-1].has_type_annotation = True
        func_obj.args[-1].has_type_comment = True
        func_obj.is_return_annotated = True

        return func_obj

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
    ) -> Union[ClassDecoratorType, None]:
        """
        Get the class method's decorator type from its function node.

        For the purposes of this tool, only @classmethod and @staticmethod decorators are
        identified; all other decorators are ignored

        If @classmethod or @staticmethod decorators are not present, this function will return None
        """
        decorators = []
        for decorator in function_node.decorator_list:
            # @classmethod and @staticmethod will show up as ast.Name objects, where callable
            # decorators will show up as ast.Call, which we can ignore
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)

        if "classmethod" in decorators:
            return ClassDecoratorType.CLASSMETHOD
        elif "staticmethod" in decorators:
            return ClassDecoratorType.STATICMETHOD
        else:
            return None


class FunctionVisitor(ast.NodeVisitor):
    """An ast.NodeVisitor instance for walking the AST and describing all contained functions."""

    def __init__(self, lines: List[str]):
        self.lines = lines
        self.function_definitions: List[Function] = []
        self._context: List[AST_DEF_NODES] = []

    def switch_context(self, node: AST_DEF_NODES) -> None:
        """
        Utilize a context switcher as a generic function visitor in order to track function context.

        Without keeping track of context, it's challenging to reliably differentiate class methods
        from "regular" functions, especially in the case of nested classes.

        Thank you for the inspiration @isidentical :)
        """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check for non-empty context first to prevent IndexErrors for non-nested nodes
            if self._context and isinstance(self._context[-1], ast.ClassDef):
                # Check if current context is a ClassDef node & pass the appropriate flag
                self.function_definitions.append(
                    Function.from_function_node(node, self.lines, is_class_method=True)
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
        self._context: List[AST_FUNCTION_TYPES] = []
        self._non_none_return_nodes: Set[AST_FUNCTION_TYPES] = set()

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
            if isinstance(node.value, (ast.Constant, ast.NameConstant)):
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
