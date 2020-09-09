from textwrap import dedent
from typing import NamedTuple


class OverloadDecoratorTestCase(NamedTuple):
    """Helper container for tests for the suppression of errors for `typing.overload` decorators."""

    src: str
    should_yield_error: bool


overload_decorator_test_cases = {
    "overload_decorated_attribute": OverloadDecoratorTestCase(
        src=dedent(
            """\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """
        ),
        should_yield_error=False,
    ),
    "overload_decorated_aliased_attribute": OverloadDecoratorTestCase(
        src=dedent(
            """\
            @t.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """
        ),
        should_yield_error=False,
    ),
    "overload_decorated_direct_import": OverloadDecoratorTestCase(
        src=dedent(
            """\
            @overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """
        ),
        should_yield_error=False,
    ),
    "overload_decorated_aliased_import": OverloadDecoratorTestCase(  # Aliased import not suppoerted
        src=dedent(
            """\
            @ovrld
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """
        ),
        should_yield_error=True,
    ),
    "overload_decorated_name_mismatch": OverloadDecoratorTestCase(
        src=dedent(
            """\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def bar(a):
                ...
            """
        ),
        should_yield_error=True,
    ),
}
