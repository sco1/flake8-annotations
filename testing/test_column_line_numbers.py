from itertools import zip_longest
from typing import Generator, Tuple

import pytest
import pytest_check as check
from flake8_annotations import checker
from testing.helpers import check_source

from .test_cases.column_line_numbers_test_cases import ParserTestCase, parser_test_cases

ERROR_CODE = Tuple[int, int, str, checker.TypeHintChecker]


@pytest.fixture(params=parser_test_cases.items())
def parsed_errors(
    request,  # noqa: ANN001
) -> Tuple[Generator[ERROR_CODE, None, None], ParserTestCase]:
    """
    Create a fixture for the error codes emitted by our testing code.

    `parser_test_cases` is a dictionary of ParserTestCase named tuples, which provide the
    following:
        * `src` - Source code for the test case to be parsed
        * `error_locations` - Truthe value tuple of (row number, column offset) tuples
            * Row numbers are 1-indexed
            * Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted

    The fixture provides a generator of yielded errors for the input source, along with the test
    case to use for obtaining truth values
    """
    test_case_name, test_case = request.param
    return check_source(test_case.src), test_case


def test_lineno(parsed_errors: Tuple[Generator[ERROR_CODE, None, None], ParserTestCase]) -> None:
    """
    Check for correct line number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Line numbers are 1-indexed
    """
    for should_error_idx, raised_error_code in zip_longest(
        parsed_errors[1].error_locations, parsed_errors[0]
    ):
        check.equal(should_error_idx[0], raised_error_code[0])


def test_column_offset(
    parsed_errors: Tuple[Generator[ERROR_CODE, None, None], ParserTestCase]
) -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    for should_error_idx, raised_error_code in zip_longest(
        parsed_errors[1].error_locations, parsed_errors[0]
    ):
        check.equal(should_error_idx[1], raised_error_code[1])
