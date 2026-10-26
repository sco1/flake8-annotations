from collections import abc
from textwrap import dedent
from typing import NamedTuple

from flake8_annotations.checker import _DEFAULT_OVERLOAD_DECORATORS


class OverloadDecoratorTestCase(NamedTuple):
    """Helper container for tests for the suppression of errors for `typing.overload` decorators."""

    src: str
    should_yield_error: bool
    overload_decorators: abc.Set[str] = frozenset(_DEFAULT_OVERLOAD_DECORATORS)
    allow_untyped_defs: bool = False


overload_decorator_test_cases = {
    "overload_decorated_attribute": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_decorated_aliased_attribute": OverloadDecoratorTestCase(
        src=dedent("""\
            @t.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_decorated_direct_import": OverloadDecoratorTestCase(
        src=dedent("""\
            @overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_decorated_aliased_import": OverloadDecoratorTestCase(
        src=dedent("""\
            @ovrld
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=True,
    ),
    "overload_decorated_aliased_import_configured": OverloadDecoratorTestCase(
        src=dedent("""\
            @ovrld
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
        overload_decorators={"ovrld"},
    ),
    "overload_decorated_name_mismatch": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def bar(a):
                ...
            """),
        should_yield_error=True,
    ),
    "overload_decorated_attribute_callable": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload()
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_decorated_direct_import_callable": OverloadDecoratorTestCase(
        src=dedent("""\
            @overload()
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_not_first_decorator_staticmethod": OverloadDecoratorTestCase(
        src=dedent("""\
            class Foo:
                @staticmethod
                @typing.overload
                def foo(a: int) -> int:
                    ...

                @staticmethod
                @typing.overload
                def foo(a: str) -> str:
                    ...

                @staticmethod
                def foo(a):
                    ...
            """),
        should_yield_error=False,
    ),
    "overload_not_first_decorator_abstractmethod": OverloadDecoratorTestCase(
        src=dedent("""\
            class Foo(abc.ABC):
                @abc.abstractmethod
                @typing.overload
                def foo(self: Foo, a: int) -> int:
                    ...

                @abc.abstractmethod
                @typing.overload
                def foo(self: Foo, a: str) -> str:
                    ...

                @abc.abstractmethod
                def foo(self, a):
                    ...
            """),
        should_yield_error=False,
    ),
    "overload_not_first_decorator_callable": OverloadDecoratorTestCase(
        src=dedent("""\
            @deprecated("Use something else")
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_series_followed_by_same_name_in_other_class": OverloadDecoratorTestCase(
        src=dedent("""\
            class Foo:
                @typing.overload
                def foo(self: Foo, a: int) -> int:
                    ...

                @typing.overload
                def foo(self: Foo, a: str) -> str:
                    ...

                def foo(self, a):
                    ...

            class Bar:
                def foo(self: Bar, a):
                    ...
            """),
        should_yield_error=True,
    ),
    "overload_series_followed_by_same_name_redefinition": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...

            def foo(a):
                ...
            """),
        should_yield_error=True,
    ),
    "overload_series_in_multiple_classes": OverloadDecoratorTestCase(
        src=dedent("""\
            class Foo:
                @typing.overload
                def foo(self: Foo, a: int) -> int:
                    ...

                def foo(self, a):
                    ...

            class Bar:
                @typing.overload
                def foo(self: Bar, a: int) -> int:
                    ...

                def foo(self, a):
                    ...
            """),
        should_yield_error=False,
    ),
    "overload_series_of_three": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            @typing.overload
            def foo(a: str) -> str:
                ...

            @typing.overload
            def foo(a: bytes) -> bytes:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
    ),
    "overload_later_signature_unannotated": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            @typing.overload
            def foo(a):
                ...

            def foo(a):
                ...
            """),
        should_yield_error=True,
    ),
    "overload_series_followed_by_same_name_allow_untyped_defs": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...

            def foo(a: int):
                ...
            """),
        should_yield_error=True,
        allow_untyped_defs=True,
    ),
    "overload_series_allow_untyped_defs": OverloadDecoratorTestCase(
        src=dedent("""\
            @typing.overload
            def foo(a: int) -> int:
                ...

            def foo(a):
                ...
            """),
        should_yield_error=False,
        allow_untyped_defs=True,
    ),
}
