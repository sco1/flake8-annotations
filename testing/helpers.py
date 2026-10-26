from __future__ import annotations

from collections import abc

from pytest_check import check_func

from flake8_annotations.ast_walker import Function, FunctionVisitor, ast
from flake8_annotations.checker import (
    FORMATTED_ERROR,
    TypeHintChecker,
    _DEFAULT_DISPATCH_DECORATORS,
    _DEFAULT_OVERLOAD_DECORATORS,
)


def parse_source(src: str) -> tuple[ast.Module, list[str]]:
    """Parse the provided Python source string and return an (typed AST, source) tuple."""
    tree = ast.parse(src, type_comments=True)
    lines = src.splitlines(keepends=True)

    return tree, lines


def check_source(
    src: str,
    suppress_none_returns: bool = False,
    suppress_dummy_args: bool = False,
    allow_untyped_defs: bool = False,
    allow_untyped_nested: bool = False,
    mypy_init_return: bool = False,
    allow_star_arg_any: bool = False,
    respect_type_ignore: bool = False,
    dispatch_decorators: abc.Set[str] = frozenset(_DEFAULT_DISPATCH_DECORATORS),
    overload_decorators: abc.Set[str] = frozenset(_DEFAULT_OVERLOAD_DECORATORS),
) -> abc.Generator[FORMATTED_ERROR, None, None]:
    """Helper for generating linting errors from the provided source code."""
    _, lines = parse_source(src)
    checker_instance = TypeHintChecker(None, lines)

    # Manually set flake8 configuration options, as the test suite bypasses flake8's config parser
    checker_instance.suppress_none_returning = suppress_none_returns
    checker_instance.suppress_dummy_args = suppress_dummy_args
    checker_instance.allow_untyped_defs = allow_untyped_defs
    checker_instance.allow_untyped_nested = allow_untyped_nested
    checker_instance.mypy_init_return = mypy_init_return
    checker_instance.allow_star_arg_any = allow_star_arg_any
    checker_instance.respect_type_ignore = respect_type_ignore
    checker_instance.dispatch_decorators = set(dispatch_decorators)
    checker_instance.overload_decorators = set(overload_decorators)

    return checker_instance.run()


def simplify_errors(errors: abc.Iterable[FORMATTED_ERROR]) -> list[tuple[int, str]]:
    """
    Simplify the errors yielded by the checker into a list of (line number, error code) tuples.

    Yielded errors are assumed to be tuples of the form:
      (line number, column number, error string, checker class)
    """
    return [(lineno, message.split()[0]) for lineno, _, message, _ in errors]


def functions_from_source(src: str) -> list[Function]:
    """Helper for obtaining a list of Function objects from the provided source code."""
    tree, lines = parse_source(src)
    visitor = FunctionVisitor(lines)
    visitor.visit(tree)

    return visitor.function_definitions


def find_matching_function(func_list: abc.Iterable[Function], match_name: str) -> Function:
    """
    Iterate over a list of Function objects & find the first matching named function.

    Due to the definition of the test cases, this should always return something; a `ValueError` is
    raised if a match isn't found.
    """
    for function in func_list:
        if function.name == match_name:
            return function

    raise ValueError(  # pragma: no cover
        f"No function named '{match_name}' found in the provided function list"
    )


@check_func
def check_is_empty(in_sequence: abc.Sequence, msg: str = "") -> None:
    """Check whether the input sequence is empty."""
    assert not in_sequence


@check_func
def check_is_not_empty(in_sequence: abc.Sequence, msg: str = "") -> None:
    """Check whether the input sequence is not empty."""
    assert in_sequence
