from typing import Tuple

import pytest
from flake8_annotations.error_codes import Error
from testing.helpers import check_is_empty, check_is_not_empty, check_source

from .test_cases.overload_decorator_test_cases import (
    OverloadDecoratorTestCase,
    overload_decorator_test_cases,
)


class TestOverloadDecoratorErrorSuppression:
    """Test suppression of errors for the closing def of a `typing.overload` series."""

    @pytest.fixture(
        params=overload_decorator_test_cases.items(), ids=overload_decorator_test_cases.keys()
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, OverloadDecoratorTestCase, Tuple[Error]]:
        """
        Build a fixture for the errors emitted from parsing `@overload` decorated test code.

        Fixture provides a tuple of: test case name, its corresponding
        `OverloadDecoratorTestCase` instance, and a tuple of the errors yielded by the
        checker, which should be empty if the test case's `should_yield_error` is `False`.

        To support decorator aliases, the `overload_decorators` param is optionally specified by the
        test case. If none is explicitly set, the decorator list defaults to the checker's default.
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, overload_decorators=test_case.overload_decorators)),
        )

    def test_overload_decorator_error_suppression(
        self, yielded_errors: Tuple[str, OverloadDecoratorTestCase, Tuple[Error]]
    ) -> None:
        """Test that no errors are yielded for the closing def of a `typing.overload` series."""
        test_case_name, test_case, errors = yielded_errors
        failure_msg = f"Check failed for case '{test_case_name}'"

        if test_case.should_yield_error:
            check_is_not_empty(errors, msg=failure_msg)
        else:
            check_is_empty(errors, msg=failure_msg)
