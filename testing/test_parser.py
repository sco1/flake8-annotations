import ast
from itertools import zip_longest
from pathlib import Path
from typing import List, Tuple

import pytest
import pytest_check as check
from flake8_annotations import Argument, Function, FunctionVisitor
from testing import parser_object_attributes


# Parse the source code at the module level so it only has to happen once
src_filepath = Path("./testing/code/all_args.py")
with src_filepath.open("r", encoding="utf-8") as f:
    src = f.read()

tree = ast.parse(src)
lines = src.splitlines()
VISITOR = FunctionVisitor(lines)
VISITOR.visit(tree)


class TestArgumentParsing:
    """Test for proper argument parsing from source."""

    @pytest.fixture(params=parser_object_attributes.parsed_arguments.keys())
    def argument_lists(self, request) -> Tuple[List[Argument], List[Argument]]:  # noqa
        """
        Build a pair of lists of arguments to compare and return as a (truth, parsed) tuple.

        `parser_object_attributes.parsed_arguments` is a dictionary of the arguments that should be
        parsed out of the testing source code
          * Keys are the function name, as str
          * Values are a list of Argument objects that should be parsed from the function definition

        A list of parsed Argument objects is taken from the module level source parser

        Note: For testing purposes, Argument lineno and col_offset are ignored so these are set to
        dummy values in the truth dictionary
        """
        truth_arguments = parser_object_attributes.parsed_arguments[request.param]

        # Find the function in our module level source parser & get the list of Argument objects
        for function in VISITOR.function_definitions:
            if function.name == request.param:
                parsed_arguments = function.args
                break
        else:
            # We shouldn't ever get here, but add a catch-all just in case
            parsed_arguments = None

        return truth_arguments, parsed_arguments

    def test_argument_parsing(self, argument_lists: Tuple[List[Argument], List[Argument]]) -> None:
        """
        Test argument parsing of the testing source code.

        Argument objects are provided as a tuple of (truth, source) lists.
        """
        for truth_arg, parsed_arg in zip_longest(argument_lists[0], argument_lists[1]):
            check.is_true(self._is_same_arg(truth_arg, parsed_arg))

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

    @staticmethod
    def _is_same_func(func_a: Function, func_b: Function) -> bool:
        """
        Compare two Function objects for "equality."

        Because we are testing column/line number parsing in another test, we can make this
        comparison less fragile by ignoring line & column indices and instead comparing only the
        following:
          * asdf
        """
        raise NotImplementedError
