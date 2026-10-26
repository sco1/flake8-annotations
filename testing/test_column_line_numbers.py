from itertools import zip_longest

import pytest
import pytest_check as check

from testing.helpers import check_source
from testing.test_cases.column_line_numbers_test_cases import ParserTestCase, parser_test_cases

PARAMETRIZE_TEST_CASES = pytest.mark.parametrize(
    "test_case", parser_test_cases.values(), ids=list(parser_test_cases)
)


@PARAMETRIZE_TEST_CASES
def test_lineno(test_case: ParserTestCase) -> None:
    """
    Check for correct line number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    NOTE: Line numbers are 1-indexed
    """
    for should_error_idx, raised_error_code in zip_longest(
        test_case.error_locations, check_source(test_case.src)
    ):
        check.equal(should_error_idx[0], raised_error_code[0])


@PARAMETRIZE_TEST_CASES
def test_column_offset(test_case: ParserTestCase) -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    for should_error_idx, raised_error_code in zip_longest(
        test_case.error_locations, check_source(test_case.src)
    ):
        check.equal(should_error_idx[1], raised_error_code[1])
