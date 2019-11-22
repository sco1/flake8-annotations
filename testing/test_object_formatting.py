from functools import partial
from typing import NamedTuple, Tuple, Union

import pytest
import pytest_check as check
from flake8_annotations import Argument, Function
from flake8_annotations.enums import AnnotationType


# Create a dictionary of test cases for Argument and Function __str__ and __repr__ testing
# Where keys represent the name of the test case and values are a named tuple:
#  (test_object, str_output, repr_output)
class FormatTestCase(NamedTuple):
    """Named tuple for representing our test cases."""

    test_object: Union[Argument, Function]
    str_output: str
    repr_output: str


# Define partial functions to simplify object creation
arg = partial(Argument, lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS)
func = partial(Function, name="test_func", lineno=0, col_offset=0)

formatting_test_cases = {
    "arg": FormatTestCase(
        arg(argname="test_arg"),
        "<Argument: test_arg, Annotated: False>",
        "Argument('test_arg', 0, 0, AnnotationType.ARGS, False, False, False)",
    ),
    "func_no_args": FormatTestCase(
        func(args=[arg(argname="return")]),
        "<Function: test_func, Args: [<Argument: return, Annotated: False>]>",
        (
            "Function('test_func', 0, 0, FunctionType.PUBLIC, False, None, False, False, "
            "[Argument('return', 0, 0, AnnotationType.ARGS, False, False, False)])"
        ),
    ),
    "func_has_arg": FormatTestCase(
        func(args=[arg(argname="foo"), arg(argname="return")]),
        "<Function: test_func, Args: [<Argument: foo, Annotated: False>, <Argument: return, Annotated: False>]>",  # noqa: E501
        (
            "Function('test_func', 0, 0, FunctionType.PUBLIC, False, None, False, False, "
            "[Argument('foo', 0, 0, AnnotationType.ARGS, False, False, False), "
            "Argument('return', 0, 0, AnnotationType.ARGS, False, False, False)])"
        ),
    ),
}


@pytest.fixture(params=formatting_test_cases.keys())
def build_test_cases(request) -> Tuple[FormatTestCase, str]:  # noqa: TYP001
    """
    Create a fixture for the provided test cases.

    Test cases are provided as a (test_object, str_output, repr_output) named tuple, along with a
    formatted message to use for a more explicit assertion failure
    """
    failure_msg = f"Comparison check failed for case: '{request.param}'"
    return formatting_test_cases[request.param], failure_msg


def test_str(build_test_cases: Tuple[FormatTestCase, str]) -> None:
    """Test the __str__ method for Argument and Function objects."""
    test_case, failure_msg = build_test_cases
    check.equal(str(test_case.test_object), test_case.str_output, msg=failure_msg)


def test_repr(build_test_cases: Tuple[FormatTestCase, str]) -> None:
    """Test the __repr__ method for Argument and Function objects."""
    test_case, failure_msg = build_test_cases
    check.equal(repr(test_case.test_object), test_case.repr_output, msg=failure_msg)
