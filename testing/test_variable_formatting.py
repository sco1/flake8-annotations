import ast
import re
from pathlib import Path
from typing import List, Tuple

import pytest
from flake8_annotations import checker

TEST_FILE = Path("./testing/code/variable_formatting.py")
ERROR_CODE_TYPE = Tuple[int, int, str, checker.TypeHintChecker]
SIMPLE_ERROR_CODE = Tuple[str, str]

# Error type specific matching patterns
TEST_ARG_NAMES = {"TYP001": "some_arg", "TYP002": "some_args", "TYP003": "some_kwargs"}
RE_DICT = {"TYP001": r"'(\w+)'", "TYP002": r"\*(\w+)", "TYP003": r"\*\*(\w+)"}


def _simplify_error(error_code: ERROR_CODE_TYPE) -> SIMPLE_ERROR_CODE:
    """
    Simplify the error yielded by the flake8 checker into an (error type, argument name) tuple.

    Input error codes are assumed to be tuples of the form:
    (line number, column number, error string, checker class)

    Where the error string begins with "TYPxxx" and contains the arg name in the following form:
    TYP001: '{arg name}'
    TYP002: *{arg name}
    TYP003: **{arg name}
    """
    error_type = error_code[2].split()[0]
    arg_name = re.findall(RE_DICT[error_type], error_code[2])[0]
    return error_type, arg_name


class TestArgumentFormatting:
    """Testing class for containerizing parsed error codes & running the fixtured tests."""

    with TEST_FILE.open("r") as f:
        src = f.read()

    tree = ast.parse(src)
    lines = src.splitlines()

    error_codes = [_simplify_error(error) for error in checker.TypeHintChecker(tree, lines).run()]

    batched_error_codes = {error_type: [] for error_type in TEST_ARG_NAMES.keys()}
    for code, arg_name in error_codes:
        batched_error_codes[code].append(arg_name)

    @pytest.fixture(params=TEST_ARG_NAMES.keys())
    def parsed_errors(self, request) -> Tuple[str, List[SIMPLE_ERROR_CODE]]:  # noqa
        """
        Create a fixture for the error codes emitted by our testing source code.

        Error codes are batched by type as fixture params so each error type is tested explicitly
        """
        return request.param, self.batched_error_codes[request.param]

    def test_arg_name(self, parsed_errors: Tuple[str, List[SIMPLE_ERROR_CODE]]) -> None:
        """
        Check for correctly formatted argument names.

        Error code information is provided by the fixture as an (error type, list of arg name) tuple
        """
        error_type, arg_names = parsed_errors
        assert all(TEST_ARG_NAMES[error_type] == arg_name for arg_name in arg_names)
