from pathlib import Path

import pytest
import pytest_check as check
from flake8_annotations import Function, FunctionVisitor
from testing.test_parser import _find_matching_function

# Build a dictionary of test cases, where keys are the function name and values are the boolean
# result that should come out of Function.is_fully_annotated
TEST_CASES = {
    # False
    "no_arg_no_return": False,
    "partial_arg_no_return": False,
    "partial_arg_return": False,
    "full_args_no_return": False,
    "no_args_no_return": False,
    # True
    "full_arg_return": True,
    "no_args_return": True,
}


class TestFunctionParsing:
    """Test for proper determinition of whether the parsed Function is fully annotated."""

    src_filepath = Path("./testing/code/annotation_presence.py")
    visitor = FunctionVisitor.parse_file(src_filepath)

    @pytest.fixture(params=TEST_CASES.keys())
    def functions(self, request) -> Function:  # noqa
        """
        Provide the Function object from the test source that matches the fixture parameter.

        This can return None if no matching function name is found, meaning that there is a mismatch
        between the functions in the testing source and the parameters in the module-level
        TEST_CASES constant
        """
        return _find_matching_function(self.visitor.function_definitions, request.param)

    def test_fully_annotated(self, functions: Function) -> None:
        """Check the result of Function.is_fully_annotated() against the test case's truth value."""
        failure_msg = f"Comparison check failed for function: '{functions.name}'"
        check.equal(functions.is_fully_annotated(), TEST_CASES[functions.name], msg=failure_msg)
