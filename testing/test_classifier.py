import pytest

from flake8_annotations.ast_walker import Argument, Function
from flake8_annotations.checker import classify_error
from flake8_annotations.enums import AnnotationType, FunctionType
from flake8_annotations.error_codes import Error
from testing.test_cases.classifier_object_attributes import (
    AT,
    RT,
    argument_classifications,
    return_classifications,
)


class TestReturnClassifier:
    """Test missing return annotation error classifications."""

    DUMMY_RETURN = Argument(
        argname="return", lineno=0, col_offset=0, annotation_type=AnnotationType.RETURN
    )

    @pytest.mark.parametrize(("attributes", "error_code"), return_classifications.items())
    def test_return(self, attributes: RT, error_code: type[Error]) -> None:
        """Test missing return annotation error codes."""
        test_function = Function(
            name="ReturnTest",
            lineno=0,
            col_offset=0,
            function_type=attributes.function_type,
            is_class_method=attributes.is_class_method,
            class_decorator_type=attributes.class_decorator_type,
            decorator_list=[],
            args=[self.DUMMY_RETURN],
        )

        assert isinstance(classify_error(test_function, self.DUMMY_RETURN), error_code)


class TestArgumentClassifier:
    """Test missing argument annotation error classifications."""

    # Build a dummy argument to substitute for self/cls in class methods if we're looking at the
    # other arguments
    DUMMY_ARG = Argument(
        argname="DummyArg", lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS
    )

    @pytest.mark.parametrize(("attributes", "error_code"), argument_classifications.items())
    def test_argument(self, attributes: AT, error_code: type[Error]) -> None:
        """Test missing argument annotation error codes."""
        test_argument = Argument(
            argname="TestArgument",
            lineno=0,
            col_offset=0,
            annotation_type=attributes.annotation_type,
        )

        # If we're not the first argument, add in the dummy
        if attributes.is_first_arg:
            args = [test_argument]
        else:
            args = [self.DUMMY_ARG, test_argument]

        # Functions will always have a return arg but we don't need it for this test
        # The function type doesn't factor into argument classification, so it's arbitrary here
        test_function = Function(
            name="ArgumentTest",
            lineno=0,
            col_offset=0,
            function_type=FunctionType.PUBLIC,
            is_class_method=attributes.is_class_method,
            class_decorator_type=attributes.class_decorator_type,
            decorator_list=[],
            args=args,
        )

        assert isinstance(classify_error(test_function, test_argument), error_code)
