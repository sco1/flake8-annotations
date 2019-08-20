from itertools import zip_longest
from pathlib import Path
from typing import List, Tuple, Union

import pytest
import pytest_check as check
from flake8_annotations import Argument, Function, FunctionVisitor
from testing import parser_object_attributes


class TestArgumentParsing:
    """Test for proper argument parsing from source."""

    src_filepath = Path("./testing/code/all_args.py")
    visitor = FunctionVisitor.parse_file(src_filepath)

    @pytest.fixture(params=parser_object_attributes.parsed_arguments.keys())
    def argument_lists(self, request) -> Tuple[List[Argument], List[Argument], str]:  # noqa
        """
        Build a pair of lists of arguments to compare and return as a (truth, parsed) tuple.

        `parser_object_attributes.parsed_arguments` is a dictionary of the arguments that should be
        parsed out of the testing source code:
          * Keys are the function name, as str
          * Values are a list of Argument objects that should be parsed from the function definition

        A list of parsed Argument objects is taken from the class-level source parser

        The function name is also returned in order to provide a more verbose message for a failed
        assertion

        Note: For testing purposes, Argument lineno and col_offset are ignored so these are set to
        dummy values in the truth dictionary
        """
        truth_arguments = parser_object_attributes.parsed_arguments[request.param]

        matching_func = _find_matching_function(self.visitor.function_definitions, request.param)
        if matching_func:
            parsed_arguments = matching_func.args
        else:
            # We shouldn't ever get here, but add as a catch-all
            parsed_arguments = None

        return truth_arguments, parsed_arguments, request.param

    def test_argument_parsing(
        self, argument_lists: Tuple[List[Argument], List[Argument], str]
    ) -> None:
        """
        Test argument parsing of the testing source code.

        Argument objects are provided as a tuple of (truth, source) lists
        """
        for truth_arg, parsed_arg in zip_longest(argument_lists[0], argument_lists[1]):
            failure_msg = (
                f"Comparison check failed for arg '{parsed_arg.argname}' in '{argument_lists[2]}'"
            )
            check.is_true(self._is_same_arg(truth_arg, parsed_arg), msg=failure_msg)

    @staticmethod
    def _is_same_arg(arg_a: Argument, arg_b: Argument) -> bool:
        """
        Compare two Argument objects for "equality."

        Because we are testing column/line number parsing in another test, we can make this
        comparison less fragile by ignoring line & column indices and instead comparing only the
        following:
          * argname
          * annotation_type
          * has_type_annotation
        """
        return all(
            (
                arg_a.argname == arg_b.argname,
                arg_a.annotation_type == arg_b.annotation_type,
                arg_a.has_type_annotation == arg_b.has_type_annotation,
            )
        )


class TestFunctionParsing:
    """Test for proper function parsing from source."""

    src_filepath = Path("./testing/code/all_functions.py")
    visitor = FunctionVisitor.parse_file(src_filepath)

    @pytest.fixture(params=parser_object_attributes.parsed_functions.keys())
    def functions(self, request) -> Tuple[Function, Function]:  # noqa
        """
        Build a pair of Function objects to compare and return as a (truth, parsed) tuple.

        `parser_object_attributes.parsed_functions` is a dictionary of the Functions that should be
        parsed out of the testing source code:
          * Keys are the function name, as str
          * Values are the Function object that should be parsed from the source
        """
        truth_function = parser_object_attributes.parsed_functions[request.param]

        # This should return the Function object. It may return None if no matching function name
        # is found, due to misconfigured test parameters
        parsed_function = _find_matching_function(self.visitor.function_definitions, request.param)

        return truth_function, parsed_function

    def test_function_parsing(self, functions: Tuple[Function, Function]) -> None:
        """
        Test function parsing of the testing source code.

        Function objects are provided as a (truth, source) tuple
        """
        failure_msg = f"Comparison check failed for function: '{functions[1].name}'"
        check.is_true(self._is_same_func(functions[0], functions[1]), msg=failure_msg)

    @staticmethod
    def _is_same_func(func_a: Function, func_b: Function) -> bool:
        """
        Compare two Function objects for "equality."

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


def _find_matching_function(
    function_list: List[Function], match_name: str
) -> Union[Function, None]:
    """
    Iterate over a list of Function objects & find the matching named function.

    If no function is found, this returns None
    """
    for function in function_list:
        if function.name == match_name:
            return function
