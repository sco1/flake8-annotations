import pytest
import pytest_check as check

from testing.helpers import functions_from_source
from testing.test_cases.annotation_presence_test_cases import (
    AnnotationTestCase,
    annotation_test_cases,
)


@pytest.mark.parametrize(
    "test_case", annotation_test_cases.values(), ids=list(annotation_test_cases)
)
def test_fully_annotated(test_case: AnnotationTestCase) -> None:
    """Check the result of Function.is_fully_annotated() against the test case's truth value."""
    # Each test case should define a single function
    functions = functions_from_source(test_case.src)
    assert len(functions) == 1

    function = functions[0]
    check.equal(function.is_fully_annotated(), test_case.is_fully_annotated)
