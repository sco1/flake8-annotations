from itertools import zip_longest
from pathlib import Path
from typing import List, Tuple, Union

import pytest
import pytest_check as check
from flake8_annotations import Argument, Function, FunctionVisitor
from testing import type_comment_parser_object_attributes
from testing.test_parser import _find_matching_function

ARG_FIXTURE_TYPE = Tuple[List[Argument], List[Argument], str]


class TestArgumentParsing:
    """Test for proper argument parsing from source."""

    src_filepath = Path("./testing/code/type_comments.py")
    visitor = FunctionVisitor.parse_file(src_filepath)

    @pytest.fixture(params=type_comment_parser_object_attributes.parsed_arguments.keys())
    def argument_lists(self, request) -> ARG_FIXTURE_TYPE:  # noqa
        """
        Build a pair of lists of arguments to compare and return as a (truth, parsed) tuple.

        `parser_object_attributes.parsed_arguments` is a dictionary of the arguments that should be
        parsed out of the testing source code:
          * Keys are the function name, as str
          * Values are a list of Argument objects that should be parsed from the function definition

        A list of parsed Argument objects is taken from the class-level source parser

        The function name is also returned in order to provide a more verbose message for a failed
        assertion
        """
        truth_arguments = type_comment_parser_object_attributes.parsed_arguments[request.param]

        matching_func = _find_matching_function(self.visitor.function_definitions, request.param)
        if matching_func:
            parsed_arguments = matching_func.args
        else:
            # We shouldn't ever get here, but add as a catch-all
            parsed_arguments = None

        return truth_arguments, parsed_arguments, request.param

    def test_argument_parsing(self, argument_lists: ARG_FIXTURE_TYPE) -> None:
        """
        Test argument parsing of the testing source code.

        Argument objects are provided as a tuple of (truth, source) lists
        """
        for truth_arg, parsed_arg in zip_longest(*argument_lists[:2]):
            failure_msg = (
                f"Comparison check failed for arg '{parsed_arg.argname}' in '{argument_lists[2]}'"
            )
            check.is_true(self._is_same_arg(truth_arg, parsed_arg), msg=f"{repr(truth_arg)}\n{repr(parsed_arg)}")

    @staticmethod
    def _is_same_arg(arg_a: Argument, arg_b: Argument) -> bool:
        """
        Compare two Argument objects for "equality."

        Because we are testing argument parsing in another test, we can make this comparison less
        fragile by ignoring line & column indices and instead comparing only the following:
          * argname
          * has_type_annotation
          * has_3107_annotation
          * has_type_comment
        """
        return all(
            (
                arg_a.argname == arg_b.argname,
                arg_a.has_type_annotation == arg_b.has_type_annotation,
                arg_a.has_3107_annotation == arg_b.has_3107_annotation,
                arg_a.has_type_comment == arg_b.has_type_comment
            )
        )
