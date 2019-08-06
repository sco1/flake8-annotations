import ast
from typing import List, Union

from ast_adventures.enums import AnnotationType, ClassDecoratorType, FunctionType


__version__ = "2019.0"

AST_ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")
AST_FUNCTION_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class Argument:
    """Represent a function argument & its metadata."""

    def __init__(self, argname: str, line: int, column: int, annotation_type: AnnotationType):
        self.argname = argname
        self.line = line
        self.column = column
        self.annotation_type = annotation_type
        self.has_type_annotation = False

    def __repr__(self):
        # Debugging repr
        return f"{self.argname}: {self.has_type_annotation}"

    def __str__(self):
        # Debugging print
        return (
            f"{self.argname}\n"
            f"         Line Number: {self.line}\n"
            f"       Column Number: {self.column}\n"
            f"     Annotation type: {self.annotation_type}\n"
            f"Has Type Annotation?: {self.has_type_annotation}\n"
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
        line: int,
        column: int,
        function_type: FunctionType = FunctionType.PUBLIC,
        is_class_method: bool = False,
        class_decorator_type: Union[ClassDecoratorType, None] = None,
        is_return_annotated: bool = False,
    ):
        self.name = name
        self.line = line
        self.column = column
        self.is_class_method = is_class_method
        self.function_type = function_type
        self.class_decorator_type = class_decorator_type
        self.args = None
        self.is_return_annotated = is_return_annotated

    def __repr__(self):
        # Debugging repr
        return f"{self.name}: {self.args}"

    def __str__(self):
        # Debugging print
        return (
            f"{self.name}\n"
            f"       Function type: {self.function_type}\n"
            f"         Line Number: {self.line}\n"
            f"       Column Number: {self.column}\n"
            f"       Class method?: {self.is_class_method}\n"
            f"Class decorator type: {self.class_decorator_type}\n"
            f"                Args: {self.args}\n"
            f"Is return annotated?: {self.is_return_annotated}\n"
            f" Is fully annotated?: {self.is_fully_annotated()}\n"
            f" Missing Annotations: {self.get_missed_annotations()}\n"
        )

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
    def from_function_node(cls, node: AST_FUNCTION_TYPES, **kwargs):
        """
        Create an Function object from ast.FunctionDef or ast.AsyncFunctionDef nodes.

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
        return_arg = Argument("return", node.lineno, node.col_offset, AnnotationType.RETURN)
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

    def __init__(self):
        self.function_definitions = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Handle a visit to a function definition.

        Note: This will not contain class methods, these are included in the body of ClassDef
        statements
        """
        self.function_definitions.append(Function.from_function_node(node))
        self.generic_visit(node)  # Walk through any nested functions

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """
        Handle a visit to a coroutine definition.

        Note: This will not contain class methods, these are included in the body of ClassDef
        statements
        """
        self.function_definitions.append(Function.from_function_node(node))
        self.generic_visit(node)  # Walk through any nested functions

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Handle a visit to a class definition.

        Class methods will all be contained in the body of the node
        """
        # Use ast.NodeVisitor.generic_visit to punt class method processing to the other function
        # visitors
        self.generic_visit(node)
