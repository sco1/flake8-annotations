import pytest

from testing.helpers import check_is_empty, check_is_not_empty, check_source
from testing.test_cases.overload_decorator_test_cases import (
    OverloadDecoratorTestCase,
    overload_decorator_test_cases,
)


@pytest.mark.parametrize(
    "test_case",
    overload_decorator_test_cases.values(),
    ids=list(overload_decorator_test_cases),
)
def test_overload_decorator_error_suppression(test_case: OverloadDecoratorTestCase) -> None:
    """
    Test that no errors are yielded for the closing def of a `typing.overload` series.

    To support decorator aliases, the `overload_decorators` param is optionally specified by the
    test case. If none is explicitly set, the decorator list defaults to the checker's default.
    """
    errors = tuple(
        check_source(
            test_case.src,
            overload_decorators=test_case.overload_decorators,
            allow_untyped_defs=test_case.allow_untyped_defs,
        )
    )

    if test_case.should_yield_error:
        check_is_not_empty(errors)
    else:
        check_is_empty(errors)
