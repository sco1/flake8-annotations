from typing import Tuple

import pytest
from flake8_annotations.error_codes import Error
from testing.helpers import check_is_empty, check_is_not_empty, check_source

from .test_cases.dispatch_decorator_test_cases import (
    DispatchDecoratorTestCase,
    dispatch_decorator_test_cases,
)


class TestDispatchDecoratorErrorSuppression:
    """Test suppression of errors for the dispatch decorated functions."""

    @pytest.fixture(
        params=dispatch_decorator_test_cases.items(), ids=dispatch_decorator_test_cases.keys()
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, DispatchDecoratorTestCase, Tuple[Error]]:
        """
        Build a fixture for the errors emitted from parsing dispatch decorated test code.

        Fixture provides a tuple of: test case name, its corresponding
        `DispatchDecoratorTestCase` instance, and a tuple of the errors yielded by the
        checker, which should be empty if the test case's `should_yield_error` is `False`.

        To support decorator aliases, the `dispatch_decorators` param is optionally specified by the
        test case. If none is explicitly set, the decorator list defaults to the checker's default.
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, dispatch_decorators=test_case.dispatch_decorators)),
        )

    def test_dispatch_decorator_error_suppression(
        self, yielded_errors: Tuple[str, DispatchDecoratorTestCase, Tuple[Error]]
    ) -> None:
        """Test that no errors are yielded dispatch decorated functions."""
        test_case_name, test_case, errors = yielded_errors
        failure_msg = f"Check failed for case '{test_case_name}'"

        if test_case.should_yield_error:
            check_is_not_empty(errors, msg=failure_msg)
        else:
            check_is_empty(errors, msg=failure_msg)
