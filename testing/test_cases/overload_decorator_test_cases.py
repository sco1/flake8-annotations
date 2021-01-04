from textwrap import dedent
from typing import AbstractSet, NamedTuple

from flake8_annotations.checker import _DEFAULT_OVERLOAD_DECORATORS


class OverloadDecoratorTestCase(NamedTuple):
    """Helper container for tests for the suppression of errors for `typing.overload` decorators."""

    src: str
    should_yield_error: bool
    overload_decorators: AbstractSet[str] = frozenset(_DEFAULT_OVERLOAD_DECORATORS)


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
    "overload_decorated_aliased_import": OverloadDecoratorTestCase(
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
    "overload_decorated_aliased_import_configured": OverloadDecoratorTestCase(
        src=dedent(
            """\
            @ovrld
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """
        ),
        should_yield_error=False,
        overload_decorators={"ovrld"},
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
