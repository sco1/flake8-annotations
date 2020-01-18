from typing import Generator, Iterable, List, Optional, Tuple

from flake8_annotations import Function, FunctionVisitor, PY_GTE_38
from flake8_annotations.checker import TypeHintChecker
from flake8_annotations.error_codes import Error

if PY_GTE_38:
    import ast
else:
    from typed_ast import ast3 as ast


def parse_source(src: str) -> Tuple[ast.Module, List[str]]:
    """Parse the provided Python source string and return an (typed AST, source) tuple."""
    if PY_GTE_38:
        # Built-in ast requires a flag to parse type comments
        tree = ast.parse(src, type_comments=True)
    else:
        # typed-ast will implicitly parse type comments
        tree = ast.parse(src)

    lines = src.splitlines(keepends=True)

    return tree, lines


def check_source(src: str) -> Generator[Error, None, None]:
    """Helper for generating linting errors from the provided source code."""
    _, lines = parse_source(src)
    checker_instance = TypeHintChecker(None, lines)

    # Hardcode None return suppression since our test suite bypasses flake8's configuration parser
    # None return suppression is tested explicitly in its own test suite
    checker_instance.suppress_none_returning = False

    return checker_instance.run()


def functions_from_source(src: str) -> List[Function]:
    """Helper for obtaining a list of Function objects from the provided source code."""
    tree, lines = parse_source(src)
    visitor = FunctionVisitor(lines)
    visitor.visit(tree)

    return visitor.function_definitions


def find_matching_function(func_list: Iterable[Function], match_name: str) -> Optional[Function]:
    """
    Iterate over a list of Function objects & find the first matching named function.

    Due to the definition of the test cases, this should always return something, but there is no
    protection if a match isn't found & will raise an `IndexError`.
    """
    return [function for function in func_list if function.name == match_name][0]
