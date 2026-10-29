import pytest
import pytest_check as check

from testing.helpers import check_source
from testing.test_cases.none_return_suppress_test_cases import (
    NoneReturnSuppressionTestCase,
    return_suppression_test_cases,
)


@pytest.mark.parametrize(
    "test_case", return_suppression_test_cases.values(), ids=list(return_suppression_test_cases)
)
def test_suppressed_return_error(test_case: NoneReturnSuppressionTestCase) -> None:
    """Test that ANN200 level errors are suppressed if a function only returns None."""
    errors = check_source(test_case.src, suppress_none_returns=True)

    yielded_ANN200 = any("ANN2" in error[2] for error in errors)
    check.equal(test_case.should_yield_ANN200, yielded_ANN200)
