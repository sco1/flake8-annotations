from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations.error_codes import Error
from testing.helpers import check_source

from .test_cases.none_return_suppress_test_cases import (
    NoneReturnSuppressionTestCase,
    return_suppression_test_cases,
)


class TestNoneReturnErrorSuppression:
    """Test suppression of None returns."""

    @pytest.fixture(
        params=return_suppression_test_cases.items(), ids=return_suppression_test_cases.keys()
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, NoneReturnSuppressionTestCase, Tuple[Error]]:
        """
        Build a fixture for the error codes emitted from parsing the None return test code.

        Fixture provides a tuple of: test case name, its corresponding NoneReturnSuppressionTestCase
        instance, and a tuple of the errors yielded by the checker
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, suppress_none_returns=True)),
        )

    def test_suppressed_return_error(
        self, yielded_errors: Tuple[str, NoneReturnSuppressionTestCase, Tuple[Error]]
    ) -> None:
        """Test that ANN200 level errors are suppressed if a function only returns None."""
        failure_msg = f"Check failed for case '{yielded_errors[0]}'"

        yielded_ANN200 = any("ANN2" in error[2] for error in yielded_errors[2])
        check.equal(yielded_errors[1].should_yield_ANN200, yielded_ANN200, msg=failure_msg)
