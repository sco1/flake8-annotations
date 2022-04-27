from textwrap import dedent

import pytest

from testing.helpers import check_source

TEST_CASES = (
    (
        dedent(
            """\
            def foo(a):
                # type: int -> None
                ...
            """
        ),
        3,
        1,
    ),
    (
        dedent(
            """\
            def foo(
                a  # type: int
            ):
                ...
            """
        ),
        3,
        1,
    ),
    (
        dedent(
            """\
            def foo(
                a  # type: int
            ):
                # type: (...) -> int
                ...
            """
        ),
        4,
        2,
    ),
)


@pytest.mark.parametrize(("src", "n_errors", "n_ann402"), TEST_CASES)
def test_dynamic_typing_errors(src: str, n_errors: int, n_ann402: int) -> None:
    found_errors = list(check_source(src))
    assert len(found_errors) == n_errors

    assert sum("ANN402" in err[2] for err in found_errors) == n_ann402
