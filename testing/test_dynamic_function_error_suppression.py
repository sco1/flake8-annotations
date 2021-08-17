from typing import Tuple

import pytest

from flake8_annotations.error_codes import Error
from testing.helpers import check_is_empty, check_is_not_empty, check_source
from .test_cases.dynamic_function_test_cases import (
    DynamicallyTypedFunctionTestCase,
    DynamicallyTypedNestedFunctionTestCase,
    dynamic_function_test_cases,
    nested_dynamic_function_test_cases,
)


class TestDynamicallyTypedFunctionErrorSuppression:
    """Test suppression of errors for dynamically typed functions."""

    @pytest.fixture(
        params=dynamic_function_test_cases.items(), ids=dynamic_function_test_cases.keys()
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, DynamicallyTypedFunctionTestCase, Tuple[Error]]:
        """
        Build a fixture for the errors emitted from parsing the dynamically typed def test code.

        Fixture provides a tuple of: test case name, its corresponding
        `DynamicallyTypedFunctionTestCase` instance, and a tuple of the errors yielded by the
        checker, which should be empty if the test case's `should_yield_error` is `False`.
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, allow_untyped_defs=True)),
        )

    def test_suppressed_dynamic_function_error(
        self, yielded_errors: Tuple[str, DynamicallyTypedFunctionTestCase, Tuple[Error]]
    ) -> None:
        """Test that all errors are suppressed if a function is dynamically typed."""
        test_case_name, test_case, errors = yielded_errors
        failure_msg = f"Check failed for case '{test_case_name}'"

        if test_case.should_yield_error:
            check_is_not_empty(errors, msg=failure_msg)
        else:
            check_is_empty(errors, msg=failure_msg)


class TestDynamicallyTypedNestedFunctionErrorSuppression:
    """Test suppression of errors for dynamically typed nested functions."""

    @pytest.fixture(
        params=nested_dynamic_function_test_cases.items(),
        ids=nested_dynamic_function_test_cases.keys(),
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, DynamicallyTypedNestedFunctionTestCase, Tuple[Error]]:
        """
        Build a fixture for the errors emitted from parsing the dynamically typed def test code.

        Fixture provides a tuple of: test case name, its corresponding
        `DynamicallyTypedNestedFunctionTestCase` instance, and a tuple of the errors yielded by the
        checker, which should be empty if the test case's `should_yield_error` is `False`.
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, allow_untyped_nested=True)),
        )

    def test_suppressed_dynamic_nested_function_error(
        self, yielded_errors: Tuple[str, DynamicallyTypedNestedFunctionTestCase, Tuple[Error]]
    ) -> None:
        """Test that all errors are suppressed if a nested function is dynamically typed."""
        test_case_name, test_case, errors = yielded_errors
        failure_msg = f"Check failed for case '{test_case_name}'"

        if test_case.should_yield_error:
            check_is_not_empty(errors, msg=failure_msg)
        else:
            check_is_empty(errors, msg=failure_msg)
