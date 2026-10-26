import pytest

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
    linenos = [error[0] for error in check_source(test_case.src)]
    TRUTH_LINENOS = [location[0] for location in test_case.error_locations]
    assert linenos == TRUTH_LINENOS


@PARAMETRIZE_TEST_CASES
def test_column_offset(test_case: ParserTestCase) -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    col_offsets = [error[1] for error in check_source(test_case.src)]
    TRUTH_OFFSETS = [location[1] for location in test_case.error_locations]
    assert col_offsets == TRUTH_OFFSETS
