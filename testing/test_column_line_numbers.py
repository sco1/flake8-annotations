import ast
from pathlib import Path
from typing import List, Tuple

import pytest
from flake8_annotations import checker


TEST_FILE = Path("./testing/code/column_line_numbers.py")

# (line, column) tuples where we should get linting errors in the test file
# Line numbers are 1-indexed
# Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
SHOULD_ERROR = ((16, 8), (16, 11), (24, 4), (25, 4), (26, 2))
ERROR_CODE_TYPE = Tuple[int, int, str, checker.TypeHintChecker]


@pytest.fixture
def parsed_errors(src_filepath: Path = TEST_FILE) -> List[ERROR_CODE_TYPE]:
    """Create a fixture for our the error codes emitted by our testing code."""
    with src_filepath.open("r") as f:
        src = f.read()

    tree = ast.parse(src)
    lines = src.splitlines()

    return list(checker.TypeHintChecker(tree, lines).run())


def test_lineno(parsed_errors: List[ERROR_CODE_TYPE]) -> None:
    """
    Check for correct line number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Line numbers are 1-indexed
    """
    should_error_lines = [coordinate_pair[0] for coordinate_pair in SHOULD_ERROR]
    raised_error_lines = [error_tuple[0] for error_tuple in parsed_errors]

    assert should_error_lines == raised_error_lines


def test_column_offset(parsed_errors: List[ERROR_CODE_TYPE]) -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    should_error_columns = [coordinate_pair[1] for coordinate_pair in SHOULD_ERROR]
    raised_error_columns = [error_tuple[1] for error_tuple in parsed_errors]

    assert should_error_columns == raised_error_columns
