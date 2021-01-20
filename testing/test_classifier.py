from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations import Argument, Function
from flake8_annotations.checker import FORMATTED_ERROR, classify_error
from flake8_annotations.enums import AnnotationType
from flake8_annotations.error_codes import Error
from testing.helpers import check_source

from .test_cases import classifier_object_attributes
from .test_cases.type_comment_test_cases import ParserTestCase, parser_test_cases


class TestReturnClassifier:
    """Test missing return annotation error classifications."""

    dummy_arg = Argument(
        argname="return", lineno=0, col_offset=0, annotation_type=AnnotationType.RETURN
    )

    @pytest.fixture(params=classifier_object_attributes.return_classifications.keys())
    def function_builder(self, request) -> Tuple[Function, Error]:  # noqa: ANN001
        """
        Build a Function object from the fixtured parameters.

        `classifier_object_attributes.return_classifications` is a dictionary of possible function
        combinations along with the resultant error code:
          * Keys are named tuples of the form:
              (function_type, is_class_method, class_decorator_type)
          * Values are the error object that should be returned by the error classifier
        """
        error_object = classifier_object_attributes.return_classifications[request.param]
        function_object = Function(
            name="ReturnTest",
            lineno=0,
            col_offset=0,
            function_type=request.param.function_type,
            is_class_method=request.param.is_class_method,
            class_decorator_type=request.param.class_decorator_type,
        )
        return function_object, error_object

    def test_return(self, function_builder: Tuple[Function, Error]) -> None:
        """Test missing return annotation error codes."""
        test_function, error_object = function_builder
        assert isinstance(classify_error(test_function, self.dummy_arg), error_object)


class TestArgumentClassifier:
    """Test missing argument annotation error classifications."""

    # Build a dummy argument to substitute for self/cls in class methods if we're looking at the
    # other arguments
    dummy_arg = Argument(argname="DummyArg", lineno=0, col_offset=0, annotation_type=None)

    @pytest.fixture(params=classifier_object_attributes.argument_classifications.keys())
    def function_builder(self, request) -> Tuple[Function, Argument, Error]:  # noqa: ANN001
        """
        Build function and argument objects from the fixtured parameters.

        `classifier_object_attributes.argument_classifications` is a dictionary of possible argument
        and function combinations along with the resultant error code:
          * Keys are tuples of the form:
              (is_class_method, is_first_arg, classs_decorator_type, annotation_type)
          * Values are the error object that should be returned by the error classifier
        """
        error_object = classifier_object_attributes.argument_classifications[request.param]
        function_object = Function(
            name="ArgumentTest",
            lineno=0,
            col_offset=0,
            function_type=None,
            is_class_method=request.param.is_class_method,
            class_decorator_type=request.param.class_decorator_type,
        )
        argument_object = Argument(
            argname="TestArgument",
            lineno=0,
            col_offset=0,
            annotation_type=request.param.annotation_type,
        )

        # Build dummy function object arguments
        if request.param.is_first_arg:
            function_object.args = [argument_object]
        else:
            # If we're not the first argument, add in the dummy
            function_object.args = [self.dummy_arg, argument_object]

        return function_object, argument_object, error_object

    def test_argument(self, function_builder: Tuple[Function, Argument, Error]) -> None:
        """Test missing argument annotation error codes."""
        test_function, test_argument, error_object = function_builder
        assert isinstance(classify_error(test_function, test_argument), error_object)


class TestMixedTypeHintClassifier:
    """Test for correct classification of mixed type comments & type annotations."""

    @pytest.fixture(params=parser_test_cases.items(), ids=parser_test_cases.keys())
    def yielded_errors(
        self, request  # noqa: ANN001
    ) -> Tuple[str, ParserTestCase, Tuple[FORMATTED_ERROR]]:
        """
        Build a fixture for the error codes emitted from parsing the type comments test code.

        Fixture provides a tuple of: test case name, its corresponding ParserTestCase instance, and
        a tuple of the errors yielded by the checker
        """
        test_case_name, test_case = request.param

        return test_case_name, test_case, tuple(check_source(test_case.src))

    def test_ANN301_classification(
        self, yielded_errors: Tuple[str, ParserTestCase, Tuple[FORMATTED_ERROR]]
    ) -> None:
        """Test for correct classification of mixed type comments & type annotations."""
        failure_msg = f"Check failed for case '{yielded_errors[0]}'"

        yielded_ANN301 = any("ANN301" in error[2] for error in yielded_errors[2])
        check.equal(yielded_errors[1].should_yield_ANN301, yielded_ANN301, msg=failure_msg)

    def test_single_ANN301_yield(
        self, yielded_errors: Tuple[str, ParserTestCase, Tuple[FORMATTED_ERROR]]
    ) -> None:
        """Test that only one ANN301 error is yielded if a function mixes type comments."""
        if yielded_errors[1].should_yield_ANN301:
            n_yielded_ANN301_errors = sum("ANN301" in error[2] for error in yielded_errors[2])
            assert n_yielded_ANN301_errors == 1
