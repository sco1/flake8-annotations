import ast
from typing import List, Union

from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType


__version__ = "1.0.0"

AST_ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")
AST_FUNCTION_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef]

# Valid methods for property decorators
# .getter is included for completeness, even though it overrides the @property decorated method if
# you use them together
PROPERTY_METHODS = ("getter", "setter", "deleter")


class Argument:
    """Represent a function argument & its metadata."""

    def __init__(self, argname: str, lineno: int, col_offset: int, annotation_type: AnnotationType):
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
        self.annotation_type = annotation_type
        self.has_type_annotation = False

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

    def _debug_summary(self) -> str:
        """Generate a table of Argument's attributes for debugging purposes"""
        return (
            f"{self.argname}\n"
            f"         Line Number: {self.lineno}\n"
            f"       Column Number: {self.col_offset}\n"
            f"     Annotation type: {self.annotation_type}\n"
            f"Has Type Annotation?: {self.has_type_annotation}\n"
        )


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
    ):
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.is_class_method = is_class_method
        self.function_type = function_type
        self.class_decorator_type = class_decorator_type
        self.args = None
        self.is_return_annotated = is_return_annotated

    def is_fully_annotated(self) -> bool:
        """
        Check that all of the function's inputs are type annotated.

        Note that self.args will always include an Argument object for return
        """
        return all(arg.has_type_annotation for arg in self.args)

    def get_missed_annotations(self) -> List:
        """Provide a list of arguments with missing type annotations."""
        return [arg for arg in self.args if not arg.has_type_annotation]

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
        # Calculate the column offset of the end of the function definition by finding where : is
        # Lineno is 1-indexed, the line string is 0-indexed
        def_end_col_offset = lines[def_end_lineno - 1].find(":") + 1
        if def_end_col_offset == -1:
            # Fallback if we've messed up our line indexing
            def_end_col_offset = node.col_offset

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
          1. Magic: function name prefixed & suffixed by "__"
          2. Private: function name prefixed by "__"
          3. Protected: function name prefixed by "_"
          4. Public: everything else
        """
        if function_name.startswith("__") and function_name.endswith("__"):
            return FunctionType.MAGIC
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
        decorator_attributes = []
        for decorator in function_node.decorator_list:
            # @property, @classmethod, and @staticmethod will be ast.Name objects
            # property.setter, and property.deleter will be ast.Attribute objects
            # Other callable decorators will be ast.Call objects, which we're ignoring
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorator_attributes.append(decorator.attr)

        if "classmethod" in decorators:
            return ClassDecoratorType.CLASSMETHOD
        elif "staticmethod" in decorators:
            return ClassDecoratorType.STATICMETHOD
        elif "property" in decorators or Function._is_property_method(decorator_attributes):
            return ClassDecoratorType.PROPERTY
        else:
            return None

    def _debug_summary(self) -> str:
        """Generate a table of Function's attributes for debugging purposes"""
        return (
            f"{self.name}\n"
            f"       Function type: {self.function_type}\n"
            f"         Line Number: {self.lineno}\n"
            f"       Column Number: {self.col_offset}\n"
            f"       Class method?: {self.is_class_method}\n"
            f"Class decorator type: {self.class_decorator_type}\n"
            f"                Args: {self.args}\n"
            f"Is return annotated?: {self.is_return_annotated}\n"
            f" Is fully annotated?: {self.is_fully_annotated()}\n"
            f" Missing Annotations: {self.get_missed_annotations()}\n"
        )

    @staticmethod
    def _is_property_method(attribute_decorators: List[ast.Attribute]) -> bool:
        """Check the list of decorator attribute names for .setter and .deleter methods."""
        # Short circuit
        if not attribute_decorators:
            return False

        return any(property_method in attribute_decorators for property_method in PROPERTY_METHODS)


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
