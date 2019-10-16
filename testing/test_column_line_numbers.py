import sys
from itertools import zip_longest
from pathlib import Path
from typing import Generator, Tuple

import pytest
import pytest_check as check
from flake8_annotations import checker

# Check if we can use the stdlib ast module instead of typed_ast
# stdlib ast gains native type comment support in Python 3.8
if sys.version_info >= (3, 8):
    import ast
    from ast import Ellipsis as ast_Ellipsis
else:
    from typed_ast import ast3 as ast


TEST_FILE = Path("./testing/code/column_line_numbers.py")

# (line, column) tuples where we should get linting errors in the test file
# Line numbers are 1-indexed
# Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
SHOULD_ERROR = ((20, 8), (20, 11), (28, 4), (29, 4), (30, 2), (34, 10), (39, 11))
ERROR_CODE = Tuple[int, int, str, checker.TypeHintChecker]


@pytest.fixture
def parsed_errors(src_filepath: Path = TEST_FILE) -> Generator[ERROR_CODE, None, None]:
    """Create a fixture for the error codes emitted by our testing code."""
    tree = checker.TypeHintChecker.load_file(src_filepath)
    return checker.TypeHintChecker(tree, src_filepath).run()


def test_lineno(parsed_errors: Generator[ERROR_CODE, None, None]) -> None:
    """
    Check for correct line number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Line numbers are 1-indexed
    """
    for should_error_idx, raised_error_code in zip_longest(SHOULD_ERROR, parsed_errors):
        check.equal(should_error_idx[0], raised_error_code[0])


def test_column_offset(parsed_errors: Generator[ERROR_CODE, None, None]) -> None:
    """
    Check for correct column number values.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """
    for should_error_idx, raised_error_code in zip_longest(SHOULD_ERROR, parsed_errors):
        check.equal(should_error_idx[1], raised_error_code[1])
