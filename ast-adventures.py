import ast
from enum import Enum, auto
from typing import Union


AST_ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")
AST_NODE_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
AST_FUNCTION_TYPES = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class MethodType(Enum):
    PUBLIC = auto()
    PROTECTED = auto()  # Leading single underscore
    PRIVATE = auto()  # Leading double underscore
    MAGIC = auto()  # Leading & trailing double underscore


class ClassMethodType(Enum):
    REGULAR = auto()
    CLASSMETHOD = auto()
    STATICMETHOD = auto()


class Argument:
    def __init__(self, argname: str):
        self.argname = argname
        self.has_type_annotation = None
        self.line = None
        self.column = None

    def __repr__(self):
        return f"{self.argname}: {self.has_type_annotation}"

    @classmethod
    def from_arg_node(cls, node: ast.arguments):
        new_arg = cls(node.arg)

        if node.annotation:
            new_arg.has_type_annotation = True
        else:
            new_arg.has_type_annotation = False

        return new_arg


class Function:
    def __init__(
        self,
        name: str,
        is_method: bool = False,
        method_type: MethodType = MethodType.PUBLIC,
        class_method_type: Union[ClassMethodType, None] = None,
        is_nested: bool = False,
    ):
        self.name = name
        self.args = {arg: None for arg in AST_ARG_TYPES}
        self.is_class_method = is_method
        self.method_type = method_type
        self.class_method_type = class_method_type
        self.is_nested = is_nested

    def __repr__(self):
        return f"{self.name}: {self.args}"

    @classmethod
    def from_function_node(cls, node: AST_NODE_TYPES, **kwargs):
        print(f"{ast.dump(node)}\n")  # Debug

        # Extract function types from function name
        kwargs["method_type"] = cls.get_function_types(node.name)
        if kwargs.get("is_class_method", False):
            kwargs["class_method_type"] = cls.get_class_method_type(node)

        new_function = cls(node.name, **kwargs)

        # Iterate over arguments by type & add
        for arg_type in AST_ARG_TYPES:
            args = node.args.__getattribute__(arg_type)
            if args:
                if not isinstance(args, list):
                    args = [args]
                new_function.args[arg_type] = [Argument.from_arg_node(arg) for arg in args]

        return new_function

    @staticmethod
    def get_function_type(function_name: str) -> MethodType:
        raise NotImplementedError

    @staticmethod
    def get_class_method_type(function_name: AST_NODE_TYPES) -> MethodType:
        raise NotImplementedError


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.definitions = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.definitions.append(Function.from_function_node(node))

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.definitions.append(Function.from_function_node(node))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        method_nodes = [
            child_node
            for child_node in node.body
            if isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        self.definitions.extend(
            [
                Function.from_function_node(method_node, is_method=True)
                for method_node in method_nodes
            ]
        )


with open("test.py", "r") as f:
    tree = ast.parse(f.read())

top_level = Visitor()
top_level.visit(tree)
print(top_level.definitions)
