import ast
from pathlib import Path
from typing import List, Union

from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType


__version__ = "1.0.1"

AST_ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")
AST_FUNCTION_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class Argument:
    """Represent a function argument & its metadata."""

    def __init__(
        self,
        argname: str,
        lineno: int,
        col_offset: int,
        annotation_type: AnnotationType,
        has_type_annotation: bool = False,
    ):
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
        self.annotation_type = annotation_type
        self.has_type_annotation = has_type_annotation

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
            "Argument"
            f"({self.argname!r}, {self.lineno}, {self.col_offset}, {self.annotation_type}, {self.has_type_annotation})"  # noqa
        )

    @classmethod
    def from_arg_node(cls, node: ast.arguments, annotation_type_name: str):
        """Create an Argument object from an ast.arguments node."""
        annotation_type = AnnotationType[annotation_type_name]
        new_arg = cls(node.arg, node.lineno, node.col_offset, annotation_type)

        if node.annotation:
            new_arg.has_type_annotation = True
        else:
            new_arg.has_type_annotation = False

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
        args: List[Argument] = None,
    ):
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.function_type = function_type
        self.is_class_method = is_class_method
        self.class_decorator_type = class_decorator_type
        self.is_return_annotated = is_return_annotated
        self.args = args

    def is_fully_annotated(self) -> bool:
        """
        Check that all of the function's inputs are type annotated.

        Note that self.args will always include an Argument object for return
        """
        return all(arg.has_type_annotation for arg in self.args)

    def get_missed_annotations(self) -> List:
        """Provide a list of arguments with missing type annotations."""
        return [arg for arg in self.args if not arg.has_type_annotation]

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
            f"Function({self.name!r}, {self.lineno}, {self.col_offset}, {self.is_class_method}, "
            f"{self.function_type}, {self.class_decorator_type}, {self.args}, {self.is_return_annotated})"  # noqa
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
        # Get the line number from the line before where the body of the function starts to account
        # for the presence of decorators
        def_end_lineno = node.body[0].lineno - 1
        while True:
            # To account for multiline docstrings, rewind through the lines until we find the line
            # containing the :
            colon_loc = lines[def_end_lineno - 1].find(":")
            if colon_loc == -1:
                def_end_lineno -= 1
            else:
                # Lineno is 1-indexed, the line string is 0-indexed
                def_end_col_offset = colon_loc + 1
                break

        return_arg = Argument("return", def_end_lineno, def_end_col_offset, AnnotationType.RETURN)
        if node.returns:
            return_arg.has_type_annotation = True
            new_function.is_return_annotated = True

        new_function.args.append(return_arg)
        return new_function

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
        function_node: AST_FUNCTION_TYPES
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
        self.function_definitions = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Handle a visit to a function definition.

        Note: This will not contain class methods, these are included in the body of ClassDef
        statements
        """
        self.function_definitions.append(Function.from_function_node(node, self.lines))
        self.generic_visit(node)  # Walk through any nested functions

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """
        Handle a visit to a coroutine definition.

        Note: This will not contain class methods, these are included in the body of ClassDef
        statements
        """
        self.function_definitions.append(Function.from_function_node(node, self.lines))
        self.generic_visit(node)  # Walk through any nested functions

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Handle a visit to a class definition.

        Class methods will all be contained in the body of the node
        """
        # Use ast.NodeVisitor.generic_visit to punt class method processing to the other function
        # visitors
        method_nodes = [
            child_node
            for child_node in node.body
            if isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        self.function_definitions.extend(
            [
                Function.from_function_node(method_node, self.lines, is_class_method=True)
                for method_node in method_nodes
            ]
        )

    @classmethod
    def parse_file(cls, src_filepath: Path) -> "FunctionVisitor":  # Need to quote for 3.6 compat
        """Return a parsed AST for the provided Python source file."""
        with src_filepath.open("r", encoding="utf-8") as f:
            src = f.read()

        tree = ast.parse(src)
        lines = src.splitlines()

        visitor = cls(lines)
        visitor.visit(tree)

        return visitor
