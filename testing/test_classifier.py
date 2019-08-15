from typing import Tuple

import pytest
from flake8_annotations import Argument, Function
from flake8_annotations.checker import classify_error
from flake8_annotations.enums import AnnotationType
from flake8_annotations.error_codes import Error
from testing import object_attributes


class TestReturnClassifier:
    """Test return error classifications."""

    dummy_arg = Argument("return", 0, 0, AnnotationType.RETURN)

    @pytest.fixture(params=object_attributes.return_classifications.keys())
    def function_builder(self, request) -> Tuple[Function, Error]:  # noqa
        """
        Build a Function object from the fixtured parameters.

        `object_attributes.return_classification` is a dictionary of possible function combinations
        and the resultant error code:
          * Keys are tuples of the form (function type, is class method?, class decorator type)
          * Values are the error object that should be returned by the error classifier
        """
        error_object = object_attributes.return_classifications[request.param]
        return Function("ReturnTest", 0, 0, *request.param), error_object

    def test_return(self, function_builder: Tuple[Function, Error]) -> None:  # noqa
        test_function, error_object = function_builder
        assert isinstance(classify_error(test_function, self.dummy_arg), error_object)
