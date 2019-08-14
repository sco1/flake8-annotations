import ast
from pathlib import Path

from flake8_annotations import checker


TEST_FILE = Path("./testing/code/column_line_numbers.py")

# (line, column) tuples where we should get linting errors in the test file
# Line numbers are 1-indexed
# Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
SHOULD_ERROR = ((16, 8), (16, 11), (24, 4), (25, 4), (26, 2))

with TEST_FILE.open("r") as f:
    src = f.read()

TREE = ast.parse(src)
LINES = src.splitlines()
ERROR_CODES = list(checker.TypeHintChecker(TREE, LINES).run())


def test_lineno() -> None:
    """
    Check for correct line number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Line numbers are 1-indexed
    """
    should_error_lines = [coordinate_pair[0] for coordinate_pair in SHOULD_ERROR]
    raised_error_lines = [error_tuple[0] for error_tuple in ERROR_CODES]

    assert should_error_lines == raised_error_lines


def test_column_offset() -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    should_error_columns = [coordinate_pair[1] for coordinate_pair in SHOULD_ERROR]
    raised_error_columns = [error_tuple[1] for error_tuple in ERROR_CODES]

    assert should_error_columns == raised_error_columns
