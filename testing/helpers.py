import typing as t

from flake8_annotations import Function, FunctionVisitor, PY_GTE_38
from flake8_annotations.checker import (
    FORMATTED_ERROR,
    TypeHintChecker,
    _DEFAULT_DISPATCH_DECORATORS,
    _DEFAULT_OVERLOAD_DECORATORS,
)
from pytest_check import check_func

if PY_GTE_38:
    import ast
else:
    from typed_ast import ast3 as ast


def parse_source(src: str) -> t.Tuple[ast.Module, t.List[str]]:
    """Parse the provided Python source string and return an (typed AST, source) tuple."""
    if PY_GTE_38:
        # Built-in ast requires a flag to parse type comments
        tree = ast.parse(src, type_comments=True)
    else:
        # typed-ast will implicitly parse type comments
        tree = ast.parse(src)

    lines = src.splitlines(keepends=True)

    return tree, lines


def check_source(
    src: str,
    suppress_none_returns: bool = False,
    suppress_dummy_args: bool = False,
    allow_untyped_defs: bool = False,
    allow_untyped_nested: bool = False,
    mypy_init_return: bool = False,
    dispatch_decorators: t.AbstractSet[str] = frozenset(_DEFAULT_DISPATCH_DECORATORS),
    overload_decorators: t.AbstractSet[str] = frozenset(_DEFAULT_OVERLOAD_DECORATORS),
) -> t.Generator[FORMATTED_ERROR, None, None]:
    """Helper for generating linting errors from the provided source code."""
    _, lines = parse_source(src)
    checker_instance = TypeHintChecker(None, lines)

    # Manually set flake8 configuration options, as the test suite bypasses flake8's config parser
    checker_instance.suppress_none_returning = suppress_none_returns
    checker_instance.suppress_dummy_args = suppress_dummy_args
    checker_instance.allow_untyped_defs = allow_untyped_defs
    checker_instance.allow_untyped_nested = allow_untyped_nested
    checker_instance.mypy_init_return = mypy_init_return
    checker_instance.dispatch_decorators = dispatch_decorators
    checker_instance.overload_decorators = overload_decorators

    return checker_instance.run()


def functions_from_source(src: str) -> t.List[Function]:
    """Helper for obtaining a list of Function objects from the provided source code."""
    tree, lines = parse_source(src)
    visitor = FunctionVisitor(lines)
    visitor.visit(tree)

    return visitor.function_definitions


def find_matching_function(func_list: t.Iterable[Function], match_name: str) -> Function:
    """
    Iterate over a list of Function objects & find the first matching named function.

    Due to the definition of the test cases, this should always return something, but there is no
    protection if a match isn't found & will raise an `IndexError`.
    """
    return [function for function in func_list if function.name == match_name][0]


@check_func
def check_is_empty(in_sequence: t.Sequence, msg: str = "") -> None:
    """Check whether the input sequence is empty."""
    assert not in_sequence


@check_func
def check_is_not_empty(in_sequence: t.Sequence, msg: str = "") -> None:
    """Check whether the input sequence is not empty."""
    assert in_sequence
