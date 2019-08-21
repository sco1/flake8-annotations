from typing import Tuple

import pytest
import pytest_check as check
from testing.printed_object_formatting import FormatTestCase, formatting_test_cases


@pytest.fixture(params=formatting_test_cases.keys())
def build_test_cases(request) -> Tuple[FormatTestCase, str]:  # noqa
    """
    Create a fixture for the provided test cases.

    Test cases are provided as a (test_object, str_output, repr_output) named tuple, along with a
    formatted message to use for a more explicit assertion failure
    """
    failure_msg = f"Comparison check failed for case: '{request.param}'"
    return formatting_test_cases[request.param], failure_msg


def test_str(build_test_cases: Tuple[FormatTestCase, str]) -> None:
    """Test the __str__ method for Argument and Function objects."""
    test_case, failure_msg = build_test_cases
    check.equal(str(test_case.test_object), test_case.str_output, msg=failure_msg)


def test_repr(build_test_cases: Tuple[FormatTestCase, str]) -> None:
    """Test the __repr__ method for Argument and Function objects."""
    test_case, failure_msg = build_test_cases
    check.equal(repr(test_case.test_object), test_case.repr_output, msg=failure_msg)
