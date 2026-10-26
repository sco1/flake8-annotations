import pytest

from testing.helpers import check_is_empty, check_is_not_empty, check_source
from testing.test_cases.dynamic_function_test_cases import (
    DynamicallyTypedFunctionTestCase,
    DynamicallyTypedNestedFunctionTestCase,
    dynamic_function_test_cases,
    nested_dynamic_function_test_cases,
)


@pytest.mark.parametrize(
    "test_case", dynamic_function_test_cases.values(), ids=list(dynamic_function_test_cases)
)
def test_suppressed_dynamic_function_error(test_case: DynamicallyTypedFunctionTestCase) -> None:
    """Test that all errors are suppressed if a function is dynamically typed."""
    errors = tuple(check_source(test_case.src, allow_untyped_defs=True))

    if test_case.should_yield_error:
        check_is_not_empty(errors)
    else:
        check_is_empty(errors)


@pytest.mark.parametrize(
    "test_case",
    nested_dynamic_function_test_cases.values(),
    ids=list(nested_dynamic_function_test_cases),
)
def test_suppressed_dynamic_nested_function_error(
    test_case: DynamicallyTypedNestedFunctionTestCase,
) -> None:
    """Test that all errors are suppressed if a nested function is dynamically typed."""
    errors = tuple(check_source(test_case.src, allow_untyped_nested=True))

    if test_case.should_yield_error:
        check_is_not_empty(errors)
    else:
        check_is_empty(errors)
