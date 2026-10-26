import pytest
import pytest_check as check

from flake8_annotations.ast_walker import Argument, Function
from flake8_annotations.enums import AnnotationType
from testing.helpers import find_matching_function, functions_from_source
from testing.test_cases.argument_parsing_test_cases import ArgumentTestCase, argument_test_cases
from testing.test_cases.function_parsing_test_cases import FunctionTestCase, function_test_cases


class TestArgumentParsing:
    """Test for proper argument parsing from source."""

    @pytest.mark.parametrize("case", argument_test_cases.values(), ids=list(argument_test_cases))
    def test_argument_parsing(self, case: ArgumentTestCase) -> None:
        """
        Test argument parsing of the testing source code.

        Each test case provides the source code to be parsed and a tuple of Argument objects to be
        used as truth values.

        NOTE: For testing purposes, Argument `lineno` and `col_offset` are ignored so these are set
        to dummy values in the truth dictionary
        """
        # Each test case should define a single function
        functions = functions_from_source(case.src)
        assert len(functions) == 1

        parsed_args = functions[0].args
        summarized = [self._summarize_arg(arg) for arg in parsed_args]
        TRUTH_SUMMARIZED = [self._summarize_arg(arg) for arg in case.args]

        assert summarized == TRUTH_SUMMARIZED

    @staticmethod
    def _summarize_arg(arg: Argument) -> tuple[str, AnnotationType, bool]:
        """
        Summarize an Argument object into the attributes relevant for comparison.

        Because we are testing column/line number parsing in another test, we can make this
        comparison less fragile by ignoring line & column indices and instead comparing only the
        following:
          * argname
          * annotation_type
          * has_type_annotation
        """
        return arg.argname, arg.annotation_type, arg.has_type_annotation


class TestFunctionParsing:
    """Test for proper function parsing from source."""

    @pytest.mark.parametrize("case", function_test_cases.values(), ids=list(function_test_cases))
    def test_function_parsing(self, case: FunctionTestCase) -> None:
        """
        Test function parsing of the testing source code.

        Each test case provides the source code to be parsed and a tuple of the Function objects
        that should be parsed from it, which are matched to the parsed Functions by name.
        """
        functions = functions_from_source(case.src)
        # First check that we've gotten all the expected functions
        check.equal([f.name for f in functions], [f.name for f in case.func])

        for f in functions:
            matched_truth_function = find_matching_function(case.func, f.name)
            failure_msg = f"Comparison check failed for function '{f.name}'"
            check.is_true(self._is_same_func(matched_truth_function, f), msg=failure_msg)

    @staticmethod
    def _is_same_func(func_a: Function, func_b: Function) -> bool:
        """
        Compare two Function objects for "equality".

        Because we are testing column/line number parsing in another test, along with argument
        parsing, we can simplify this comparison by comparing a subset of the Function object's
        attributes:
          * name
          * function_type
          * is_class_method
          * class_decorator_type
          * is_return_annotated
        """
        return all(
            (
                func_a.name == func_b.name,
                func_a.function_type == func_b.function_type,
                func_a.is_class_method == func_b.is_class_method,
                func_a.class_decorator_type == func_b.class_decorator_type,
                func_a.is_return_annotated == func_b.is_return_annotated,
            )
        )
