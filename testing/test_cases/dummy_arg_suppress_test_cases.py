from textwrap import dedent
from typing import NamedTuple


class DummyArgSuppressionTestCase(NamedTuple):
    """Helper container for tests for the suppression of dummy arg errors."""

    src: str
    should_yield_ANN000: bool


dummy_arg_suppression_test_cases = {
    "only_dummy_arg": DummyArgSuppressionTestCase(
        src=dedent(
            """\
            def foo(_) -> None:
                ...
            """
        ),
        should_yield_ANN000=False,
    ),
    "only_dummy_vararg": DummyArgSuppressionTestCase(
        src=dedent(
            """\
            def foo(*_) -> None:
                ...
            """
        ),
        should_yield_ANN000=False,
    ),
    "only_dummy_kwarg": DummyArgSuppressionTestCase(
        src=dedent(
            """\
            def foo(**_) -> None:
                ...
            """
        ),
        should_yield_ANN000=False,
    ),
    "dummy_with_annotated_arg": DummyArgSuppressionTestCase(
        src=dedent(
            """\
            def foo(a: int, _) -> None:
                ...
            """
        ),
        should_yield_ANN000=False,
    ),
    "nested_dummy_arg": DummyArgSuppressionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar(_) -> None:
                    ...
            """
        ),
        should_yield_ANN000=False,
    ),
}
