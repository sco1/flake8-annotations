from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations.checker import FORMATTED_ERROR
from testing.helpers import check_source

from .test_cases.dummy_arg_suppress_test_cases import (
    DummyArgSuppressionTestCase,
    dummy_arg_suppression_test_cases,
)


class TestDummyArgErrorSuppression:
    """Test suppression of None returns."""

    @pytest.fixture(
        params=dummy_arg_suppression_test_cases.items(), ids=dummy_arg_suppression_test_cases.keys()
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, DummyArgSuppressionTestCase, Tuple[FORMATTED_ERROR]]:
        """
        Build a fixture for the error codes emitted from parsing the dummy argument test code.

        Fixture provides a tuple of: test case name, its corresponding DummyArgSuppressionTestCase
        instance, and a tuple of the errors yielded by the checker
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, suppress_dummy_args=True)),
        )

    def test_suppressed_return_error(
        self, yielded_errors: Tuple[str, DummyArgSuppressionTestCase, Tuple[FORMATTED_ERROR]]
    ) -> None:
        """Test that ANN000 level errors are suppressed if an annotation is named '_'."""
        failure_msg = f"Check failed for case '{yielded_errors[0]}'"

        yielded_ANN000 = any("ANN0" in error[2] for error in yielded_errors[2])
        check.equal(yielded_errors[1].should_yield_ANN000, yielded_ANN000, msg=failure_msg)
