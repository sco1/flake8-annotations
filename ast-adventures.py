import ast
from enum import Enum, auto


class MethodType(Enum):
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
    def from_arg_node(cls, node):
        new_arg = cls(node.arg)

        if node.annotation:
            new_arg.has_type_annotation = True
        else:
            new_arg.has_type_annotation = False

        return new_arg


class Function:
    ARG_TYPES = ("args", "vararg", "kwonlyargs", "kwarg")

    def __init__(
        self,
        name: str,
        is_method: bool = False,
        method_type: MethodType = MethodType.REGULAR,
        is_nested: bool = False,
    ):
        self.name = name
        self.args = []
        self.is_method = is_method
        self.method_type = method_type
        self.is_nested = is_nested

    def __repr__(self):
        return f"{self.name}: {self.args}"

    @classmethod
    def from_function_node(cls, node, **kwargs):
        new_function = cls(node.name, **kwargs)
        for arg_type in cls.ARG_TYPES:
            args = node.args.__getattribute__(arg_type)
            if args:
                if not isinstance(args, list):
                    args = [args]
                new_function.args.extend([Argument.from_arg_node(arg) for arg in args])

        return new_function


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.definitions = []

    def visit_FunctionDef(self, node):
        self.definitions.append(Function.from_function_node(node))

    def visit_AsyncFunctionDef(self, node):
        self.definitions.append(Function.from_function_node(node))

    def visit_ClassDef(self, node):
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
