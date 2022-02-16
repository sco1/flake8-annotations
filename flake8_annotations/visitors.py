import typing as t

from flake8_annotations import PY_GTE_38, models

# Check if we can use the stdlib ast module instead of typed_ast
# stdlib ast gains native type comment support in Python 3.8
if PY_GTE_38:
    import ast
else:
    from typed_ast import ast3 as ast  # type: ignore[no-redef]

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


class FunctionVisitor(ast.NodeVisitor):
    """An ast.NodeVisitor instance for walking the AST and describing all contained functions."""

    AST_FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)

    def __init__(self, lines: t.List[str]):
        self.lines = lines
        self.function_definitions: t.List[models.Function] = []
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
                        models.Function.from_function_node(node, self.lines, is_class_method=True)
                    )
                elif isinstance(self._context[-1], self.AST_FUNC_TYPES):  # pragma: no branch
                    # Check for nested function & pass the appropriate flag
                    self.function_definitions.append(
                        models.Function.from_function_node(node, self.lines, is_nested=True)
                    )
            else:
                self.function_definitions.append(
                    models.Function.from_function_node(node, self.lines)
                )

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
