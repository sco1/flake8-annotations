from textwrap import dedent
from typing import NamedTuple


class NoneReturnSuppressionTestCase(NamedTuple):
    """Helper container for tests for the suppression of `None` return errors."""

    src: str
    should_yield_TYP200: bool


return_suppression_test_cases = {
    "no_returns": NoneReturnSuppressionTestCase(
        src=dedent(
            """\
            def foo():
                a = 2 + 2
            """
        ),
        should_yield_TYP200=False,
    ),
    "none_return": NoneReturnSuppressionTestCase(
        src=dedent(
            """\
            def foo():
                return
            """
        ),
        should_yield_TYP200=False,
    ),
    "branched_all_none_return": NoneReturnSuppressionTestCase(
        src=dedent(
            """\
            def foo():
                a = 2 + 2
                if a == 4:
                    return
                else:
                    return
            """
        ),
        should_yield_TYP200=False,
    ),
    "non_none_return": NoneReturnSuppressionTestCase(
        src=dedent(
            """\
            def foo():
                return True
            """
        ),
        should_yield_TYP200=True,
    ),
    "mixed_return": NoneReturnSuppressionTestCase(
        src=dedent(
            """\
            def foo():
                a = 2 + 2
                if a == 4:
                    return True
                else:
                    return
            """
        ),
        should_yield_TYP200=True,
    ),
}
