import pytest
import pytest_check as check

from testing.helpers import check_source
from testing.test_cases.mypy_init_return_test_cases import (
    MypyInitReturnTestCase,
    mypy_init_test_cases,
)


@pytest.mark.parametrize("test_case", mypy_init_test_cases.values(), ids=list(mypy_init_test_cases))
def test_suppressed_return_error(test_case: MypyInitReturnTestCase) -> None:
    """
    Test that ANN200 level errors are suppressed in class __init__ according to Mypy's behavior.

    Mypy allows omission of the return type hint for __init__ methods if at least one argument
    is annotated.
    """
    errors = check_source(test_case.src, mypy_init_return=True)

    yielded_ANN200 = any("ANN2" in error[2] for error in errors)
    check.equal(test_case.should_yield_return_error, yielded_ANN200)
