import pytest

from testing.helpers import check_is_empty, check_is_not_empty, check_source
from testing.test_cases.dispatch_decorator_test_cases import (
    DispatchDecoratorTestCase,
    dispatch_decorator_test_cases,
)


@pytest.mark.parametrize(
    "test_case",
    dispatch_decorator_test_cases.values(),
    ids=list(dispatch_decorator_test_cases),
)
def test_dispatch_decorator_error_suppression(test_case: DispatchDecoratorTestCase) -> None:
    """
    Test that no errors are yielded for dispatch decorated functions.

    To support decorator aliases, the `dispatch_decorators` param is optionally specified by the
    test case. If none is explicitly set, the decorator list defaults to the checker's default.
    """
    errors = tuple(check_source(test_case.src, dispatch_decorators=test_case.dispatch_decorators))

    if test_case.should_yield_error:
        check_is_not_empty(errors)
    else:
        check_is_empty(errors)
