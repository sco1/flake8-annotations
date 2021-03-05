from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations.checker import FORMATTED_ERROR
from testing.helpers import check_source

from .test_cases.type_comment_arg_injection_test_cases import (
    TypeCommentArgInjectTestCase,
    type_comment_arg_inject_test_cases,
)


class TestTypeCommentArgInject:
    """Test injection of `self` or `cls` intoto class methods."""

    @pytest.fixture(
        params=type_comment_arg_inject_test_cases.items(),
        ids=type_comment_arg_inject_test_cases.keys(),
    )
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, TypeCommentArgInjectTestCase, Tuple[FORMATTED_ERROR]]:
        """
        Build a fixture for the error codes emitted from parsing the test code.

        Fixture provides a tuple of: test case name, its corresponding TypeCommentArgInjectTestCase
        instance, and a tuple of the errors yielded by the checker.
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src)),
        )

    def test_type_comment_arg_injection(
        self, yielded_errors: Tuple[str, TypeCommentArgInjectTestCase, Tuple[FORMATTED_ERROR]]
    ) -> None:
        """Test that ANN100 errors are yielded appropriately for type comment annotated defs."""
        failure_msg = f"Check failed for case '{yielded_errors[0]}'"

        yielded_ANN100 = any("ANN1" in error[2] for error in yielded_errors[2])
        check.equal(yielded_errors[1].should_yield_ANN100, yielded_ANN100, msg=failure_msg)
