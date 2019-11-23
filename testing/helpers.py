import sys
from typing import Generator, Iterable, List, Optional, Tuple

from flake8_annotations import Function, FunctionVisitor
from flake8_annotations.checker import TypeHintChecker
from flake8_annotations.error_codes import Error

if sys.version_info >= (3, 8):
    import ast

    PY_GTE_38 = True
else:
    from typed_ast import ast3 as ast

    PY_GTE_38 = False


def parse_source(src: str) -> Tuple[ast.Module, List[str]]:
    """Parse the provided Python source string and return an (typed AST, source) tuple."""
    if PY_GTE_38:
        # Built-in ast requires a flag to parse type comments
        tree = ast.parse(src, type_comments=True)
    else:
        # typed-ast will implicitly parse type comments
        tree = ast.parse(src)

    lines = src.splitlines()

    return tree, lines


def check_source(src: str) -> Generator[Error, None, None]:
    """Helper for generating linting errors from the provided source code."""
    # Because TypeHintChecker is expecting a filename to initialize, rather than change this logic
    # we can use this file as a dummy, then update its tree & lines attributes as parsed from source
    checker_instance = TypeHintChecker(None, __file__)
    checker_instance.tree, checker_instance.lines = parse_source(src)

    return checker_instance.run()


def functions_from_source(src: str) -> List[Function]:
    """Helper for obtaining a list of Function objects from the provided source code."""
    tree, lines = parse_source(src)
    visitor = FunctionVisitor(lines)
    visitor.visit(tree)

    return visitor.function_definitions


def find_matching_function(func_list: Iterable[Function], match_name: str) -> Optional[Function]:
    """
    Iterate over a list of Function objects & find the matching named function.

    If no function is found, this returns None
    """
    for function in func_list:
        if function.name == match_name:
            return function
