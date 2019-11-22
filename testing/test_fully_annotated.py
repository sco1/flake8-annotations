from typing import Tuple

import pytest
import pytest_check as check
from flake8_annotations import Function, FunctionVisitor
from testing.annotation_presence_test_cases import annotation_test_cases, AnnotationTestCase
from testing.helpers import parse_source


class TestFunctionParsing:
    """Test for proper determinition of whether the parsed Function is fully annotated."""

    @pytest.fixture(params=annotation_test_cases.items(), ids=annotation_test_cases.keys())
    def functions(self, request) -> Tuple[Function, AnnotationTestCase, str]:  # noqa: TYP001
        """Provide the Function object from the test case source & the TestCase instance."""
        test_case_name, test_case = request.param

        tree, lines = parse_source(test_case.src)
        visitor = FunctionVisitor(lines)
        visitor.visit(tree)

        return visitor.function_definitions[0], test_case, test_case_name

    def test_fully_annotated(self, functions: Tuple[Function, AnnotationTestCase, str]) -> None:
        """Check the result of Function.is_fully_annotated() against the test case's truth value."""
        failure_msg = f"Comparison check failed for function: '{functions[2]}'"

        check.equal(
            functions[0].is_fully_annotated(), functions[1].is_fully_annotated, msg=failure_msg
        )
