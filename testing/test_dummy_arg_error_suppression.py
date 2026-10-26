import pytest
import pytest_check as check

from testing.helpers import check_source
from testing.test_cases.dummy_arg_suppress_test_cases import (
    DummyArgSuppressionTestCase,
    dummy_arg_suppression_test_cases,
)


@pytest.mark.parametrize(
    "test_case",
    dummy_arg_suppression_test_cases.values(),
    ids=list(dummy_arg_suppression_test_cases),
)
def test_suppressed_dummy_arg_error(test_case: DummyArgSuppressionTestCase) -> None:
    """Test that ANN000 level errors are suppressed if an argument is named '_'."""
    # First check that we get errors from the source before we see if the flag has an effect
    yielded_errs = check_source(test_case.src)
    assert any("ANN0" in error[2] for error in yielded_errs)

    errors = check_source(test_case.src, suppress_dummy_args=True)

    yielded_ANN000 = any("ANN0" in error[2] for error in errors)
    check.equal(test_case.should_yield_ANN000, yielded_ANN000)
