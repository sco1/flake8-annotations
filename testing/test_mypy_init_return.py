from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations.error_codes import Error
from testing.helpers import check_source

from .test_cases.mypy_init_return_test_cases import (
    MypyInitReturnTestCase,
    mypy_init_test_cases,
)


class TestMypyStyleInitReturnErrorSuppression:
    """Test Mypy-style omission of return type hints for typed __init__ methods."""

    @pytest.fixture(params=mypy_init_test_cases.items(), ids=mypy_init_test_cases.keys())
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, MypyInitReturnTestCase, Tuple[Error]]:
        """
        Build a fixture for the error codes emitted from parsing the Mypy __init__ return test code.

        Fixture provides a tuple of: test case name, its corresponding MypyInitReturnTestCase
        instance, and a tuple of the errors yielded by the checker
        """
        test_case_name, test_case = request.param

        return (
            test_case_name,
            test_case,
            tuple(check_source(test_case.src, mypy_init_return=True)),
        )

    def test_suppressed_return_error(
        self, yielded_errors: Tuple[str, MypyInitReturnTestCase, Tuple[Error]]
    ) -> None:
        """
        Test that ANN200 level errors are suppressed in class __init__ according to Mypy's behavior.

        Mypy allows omission of the return type hint for __init__ methods if at least one argument
        is annotated.
        """
        test_case_name, test_case, errors = yielded_errors
        failure_msg = f"Check failed for case '{test_case_name}'"

        yielded_ANN200 = any("ANN2" in error[2] for error in yielded_errors[2])
        check.equal(test_case.should_yield_return_error, yielded_ANN200, msg=failure_msg)
