import re

import pytest

from flake8_annotations.checker import FORMATTED_ERROR
from testing.helpers import check_source
from testing.test_cases.variable_formatting_test_cases import (
    FormatTestCase,
    variable_formatting_test_cases,
)

SIMPLE_ERROR_CODE = tuple[str, str]

# Error type specific matching patterns
TEST_ARG_NAMES = {"ANN001": "some_arg", "ANN002": "some_args", "ANN003": "some_kwargs"}
RE_DICT = {"ANN001": r"'(\w+)'", "ANN002": r"\*(\w+)", "ANN003": r"\*\*(\w+)"}


def _simplify_error(error_code: FORMATTED_ERROR) -> SIMPLE_ERROR_CODE:
    """
    Simplify the error yielded by the flake8 checker into an (error type, argument name) tuple.

    Input error codes are assumed to be tuples of the form:
    (line number, column number, error string, checker class)

    Where the error string begins with "ANNxxx" and contains the arg name in the following form:
    ANN001: '{arg name}'
    ANN002: *{arg name}
    ANN003: **{arg name}
    """
    error_type = error_code[2].split()[0]
    arg_name = re.findall(RE_DICT[error_type], error_code[2])[0]
    return error_type, arg_name


@pytest.mark.parametrize(
    "test_case",
    variable_formatting_test_cases.values(),
    ids=list(variable_formatting_test_cases),
)
def test_arg_name(test_case: FormatTestCase) -> None:
    """
    Check for correctly formatted argument names.

    Error codes for the test case source code are simplified into a list of
    (error code, argument name) tuples.
    """
    simplified_errors = [_simplify_error(error) for error in check_source(test_case.src)]

    assert all(TEST_ARG_NAMES[error_type] == arg_name for error_type, arg_name in simplified_errors)
