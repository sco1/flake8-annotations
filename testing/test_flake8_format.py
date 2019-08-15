from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations import error_codes
from flake8_annotations.checker import TypeHintChecker


ALL_ERROR_CODES = (
    error_codes.TYP001,
    error_codes.TYP002,
    error_codes.TYP003,
    error_codes.TYP101,
    error_codes.TYP102,
    error_codes.TYP201,
    error_codes.TYP202,
    error_codes.TYP203,
    error_codes.TYP204,
    error_codes.TYP205,
    error_codes.TYP206,
)


@pytest.fixture(params=ALL_ERROR_CODES)
def error_objects(request) -> Tuple[Tuple, error_codes.Error]:  # noqa
    """
    Create a fixture for the error object's tuple-formatted parameters emitted for flake8.

    Expected output should be (this is what we're testing!) a tuple with the following information:
      (line number: int, column number: int, message: str, checker type: TypeHintChecker object)
    """
    # Initialize error object
    error_object = request.param("test_arg", 0, 0)
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

    The prefix should be of the form: TYPxxx
    """
    error_tuple, error_code = error_objects
    error_message = error_tuple[2]

    # Error message should start with "TYP"
    check.is_true(error_message.startswith("TYP"))

    # Error prefix should be followed by 3 digits
    check.is_true(all(char.isdigit() for char in error_message[3:6]))

    # Error prefix should match error object's name
    check.equal(error_message[:6], type(error_code).__name__)
