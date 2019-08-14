import ast
from pathlib import Path
from typing import List, Tuple

import pytest
import pytest_check as check
from flake8_annotations import checker


TEST_FILES = {
    "TYP001": Path("./testing/code/typ001.py"),
    "TYP002": Path("./testing/code/typ002.py"),
    "TYP003": Path("./testing/code/typ003.py"),
    "TYP101": Path("./testing/code/typ101.py"),
    "TYP102": Path("./testing/code/typ102.py"),
    "TYP201": Path("./testing/code/typ201.py"),
    "TYP202": Path("./testing/code/typ202.py"),
    "TYP203": Path("./testing/code/typ203.py"),
    "TYP204": Path("./testing/code/typ204.py"),
    "TYP205": Path("./testing/code/typ205.py"),
    "TYP206": Path("./testing/code/typ206.py"),
}
EXPECTED_ERRORS = {
    "TYP001": [(10, "TYP001"), (17, "TYP001")],
    "TYP002": [],
    "TYP003": [],
    "TYP101": [],
    "TYP102": [],
    "TYP201": [],
    "TYP202": [],
    "TYP203": [],
    "TYP204": [],
    "TYP205": [],
    "TYP206": [],
}
ERROR_CODE = Tuple[int, int, str, checker.TypeHintChecker]
SIMPLE_ERROR_CODE = Tuple[int, str]


def _simplify_errors(error_codes: List[ERROR_CODE]) -> List[SIMPLE_ERROR_CODE]:
    """
    Simplify the errors yielded by the flake8 checker into a list of (lineno, error type) tuples.

    Input Error codes are assumed to be tuples of the form:
      (line number, column number, error string, checker class)

    Where the error string begins with "TYPxxx"
    """
    return [(code[0], code[2].split()[0]) for code in error_codes]


def _get_error_codes(filepath: Path) -> List[SIMPLE_ERROR_CODE]:
    """
    Run the flake8 checker on the provided source file and return a list of simplified errors.

    Emitted error codes are tuples of the form:
      (line number, column number, error string, checker class)

    Errors are simplified into (line number, error type) tuples
    """
    with filepath.open("r") as f:
        src = f.read()

    tree = ast.parse(src)
    lines = src.splitlines()
    return _simplify_errors(list(checker.TypeHintChecker(tree, lines).run()))


@pytest.fixture(params=TEST_FILES.keys())
def error_code_fixture(request) -> Tuple[List[SIMPLE_ERROR_CODE], List[SIMPLE_ERROR_CODE]]:  # noqa
    """
    Provide emitted & expected error codes for each tested error code.
    """
    return _get_error_codes(TEST_FILES[request.param]), EXPECTED_ERRORS[request.param]


def test_error_code(error_code_fixture) -> None:  # noqa
    """Test that the location & type of emitted error code(s) matches what we're expecting."""
    error_codes, expected_codes = error_code_fixture

    # Check that the number of errors is the same
    n_errors_equal = len(expected_codes) == len(error_codes)
    check.is_true(n_errors_equal)

    # If the number of errors are the same, check that they're the errors we're expecting on the
    # line that we're expecting
    if n_errors_equal:
        for actual_code, expected_code in zip(error_codes, expected_codes):
            check.equal(actual_code, expected_code)
