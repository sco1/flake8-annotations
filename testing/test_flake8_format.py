from typing import Tuple

import pytest
import pytest_check as check

from flake8_annotations import error_codes
from flake8_annotations.checker import TypeHintChecker

ALL_ERROR_CODES = (
    error_codes.ANN001,
    error_codes.ANN002,
    error_codes.ANN003,
    error_codes.ANN101,
    error_codes.ANN102,
    error_codes.ANN201,
    error_codes.ANN202,
    error_codes.ANN203,
    error_codes.ANN204,
    error_codes.ANN205,
    error_codes.ANN206,
)


@pytest.fixture(params=ALL_ERROR_CODES)
def error_objects(request) -> Tuple[Tuple, error_codes.Error]:  # noqa: ANN001
    """
    Create a fixture for the error object's tuple-formatted parameters emitted for flake8.

    Expected output should be (this is what we're testing!) a tuple with the following information:
      (line number: int, column number: int, message: str, checker type: TypeHintChecker object)
    """
    error_object = request.param(argname="test_arg", lineno=0, col_offset=0)
    return error_object.to_flake8(), error_object


def test_emitted_tuple_format(error_objects: Tuple[Tuple, error_codes.Error]) -> None:
    """
    Test that the emitted message is a tuple with the appropriate information.

    The tuple should be formatted with the following information:
      (line number: int, column number: int, message: str, checker type: TypeHintChecker object)
    """
    emitted_error = error_objects[0]

    # Emitted warning should be a tuple
    check.is_instance(emitted_error, Tuple)

    # Tuple should be of length 4
    check.equal(len(emitted_error), 4)

    # First two values should be integers
    check.is_instance(emitted_error[0], int)
    check.is_instance(emitted_error[1], int)

    # Third value should be a string
    check.is_instance(emitted_error[2], str)

    # Fourth value should be a type (not an instance) and the same as TypeHintChecker
    check.is_instance(emitted_error[3], type)
    check.equal(emitted_error[3], TypeHintChecker)


def test_emitted_message_prefix(error_objects: Tuple[Tuple, error_codes.Error]) -> None:
    """
    Test that the emitted message is prefixed with a code that matches the error object's name.

    The prefix should be of the form: ANNxxx
    """
    error_tuple, error_code = error_objects
    error_message = error_tuple[2]

    # Error message should start with "ANN"
    check.is_true(error_message.startswith("ANN"))

    # Error prefix should be followed by 3 digits
    check.is_true(all(char.isdigit() for char in error_message[3:6]))

    # Error prefix should match error object's name
    check.equal(error_message[:6], type(error_code).__name__)
