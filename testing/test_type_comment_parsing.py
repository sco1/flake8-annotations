from itertools import zip_longest
from typing import List, Tuple

import pytest
import pytest_check as check
from flake8_annotations import Argument, FunctionVisitor
from testing.helpers import parse_source

from .test_cases.type_comment_test_cases import parser_test_cases

ARG_FIXTURE_TYPE = Tuple[List[Argument], List[Argument], str]


class TestArgumentParsing:
    """Test for proper argument parsing from source."""

    @pytest.fixture(params=parser_test_cases.items())
    def argument_lists(self, request) -> ARG_FIXTURE_TYPE:  # noqa
        """
        Build a pair of lists of arguments to compare and return as a (truth, parsed) tuple.

        `parser_test_cases` is a dictionary of ParserTestCase named tuples, which provide the
        following:
            * `src` - Source code for the test case to be parsed
            * `args` - A list of Argument objects to be used as the truth values
            * `should_yield_TYP301` - Boolean flag indicating whether the source should yield TYP301

        A list of parsed Argument objects is taken from the class-level source parser

        The function name is also returned in order to provide a more verbose message for a failed
        assertion
        """
        test_case_name, test_case = request.param

        tree, lines = parse_source(test_case.src)
        visitor = FunctionVisitor(lines)
        visitor.visit(tree)
        parsed_arguments = visitor.function_definitions[0].args

        return test_case.args, parsed_arguments, test_case_name

    def test_argument_parsing(self, argument_lists: ARG_FIXTURE_TYPE) -> None:
        """
        Test argument parsing of the testing source code.

        Argument objects are provided as a tuple of (truth, source) lists
        """
        for truth_arg, parsed_arg in zip_longest(*argument_lists[:2]):
            failure_msg = (
                f"Comparison check failed for arg '{parsed_arg.argname}' in '{argument_lists[2]}'"
            )
            check.is_true(self._is_same_arg(truth_arg, parsed_arg), msg=failure_msg)

    @staticmethod
    def _is_same_arg(arg_a: Argument, arg_b: Argument) -> bool:
        """
        Compare two Argument objects for "equality".

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
                arg_a.has_type_comment == arg_b.has_type_comment,
            )
        )
