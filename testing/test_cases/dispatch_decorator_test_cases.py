from textwrap import dedent
from typing import AbstractSet, NamedTuple

from flake8_annotations.checker import _DEFAULT_DISPATCH_DECORATORS


class DispatchDecoratorTestCase(NamedTuple):
    """Helper container for tests for the suppression of errors for dispatch decorators."""

    src: str
    should_yield_error: bool
    dispatch_decorators: AbstractSet[str] = frozenset(_DEFAULT_DISPATCH_DECORATORS)


dispatch_decorator_test_cases = {
    "singledispatch_decorated_attribute": DispatchDecoratorTestCase(
        src=dedent(
            """\
            @functools.singledispatch
            def foo(a):
                print(a)

            @foo.register
            def _(a: list) -> None:
                for idx, thing in enumerate(a):
                    print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatch_decorated_aliased_attribute": DispatchDecoratorTestCase(
        src=dedent(
            """\
            @fnctls.singledispatch
            def foo(a):
                print(a)

            @foo.register
            def _(a: list) -> None:
                for idx, thing in enumerate(a):
                    print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatch_decorated_direct_import": DispatchDecoratorTestCase(
        src=dedent(
            """\
            @singledispatch
            def foo(a):
                print(a)

            @foo.register
            def _(a: list) -> None:
                for idx, thing in enumerate(a):
                    print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatch_decorated_aliased_import": DispatchDecoratorTestCase(
        src=dedent(
            """\
            @sngldsptch
            def foo(a):
                print(a)

            @foo.register
            def _(a: list) -> None:
                for idx, thing in enumerate(a):
                    print(idx, thing)
            """
        ),
        should_yield_error=True,
    ),
    "singledispatch_decorated_aliased_import_configured": DispatchDecoratorTestCase(
        src=dedent(
            """\
            @sngldsptch
            def foo(a):
                print(a)

            @foo.register
            def _(a: list) -> None:
                for idx, thing in enumerate(a):
                    print(idx, thing)
            """
        ),
        should_yield_error=False,
        dispatch_decorators={"sngldsptch"},
    ),
    "singledispatchmethod_decorated_attribute": DispatchDecoratorTestCase(
        src=dedent(
            """\
            class Foo:
                @functools.singledispatchmethod
                def foo(self, a):
                    print(a)

                @foo.register
                def _(self: "Foo", a: list) -> None:
                    for idx, thing in enumerate(a):
                        print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatchmethod_decorated_aliased_attribute": DispatchDecoratorTestCase(
        src=dedent(
            """\
            class Foo:
                @fnctls.singledispatchmethod
                def foo(self, a):
                    print(a)

                @foo.register
                def _(self: "Foo", a: list) -> None:
                    for idx, thing in enumerate(a):
                        print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatchmethod_decorated_direct_import": DispatchDecoratorTestCase(
        src=dedent(
            """\
            class Foo:
                @singledispatchmethod
                def foo(self, a):
                    print(a)

                @foo.register
                def _(self: "Foo", a: list) -> None:
                    for idx, thing in enumerate(a):
                        print(idx, thing)
            """
        ),
        should_yield_error=False,
    ),
    "singledispatchmethod_decorated_aliased_import": DispatchDecoratorTestCase(
        src=dedent(
            """\
            class Foo:
                @sngldsptchmthd
                def foo(self, a):
                    print(a)

                @foo.register
                def _(self: "Foo", a: list) -> None:
                    for idx, thing in enumerate(a):
                        print(idx, thing)
            """
        ),
        should_yield_error=True,
    ),
    "singledispatchmethod_decorated_aliased_import_configured": DispatchDecoratorTestCase(
        src=dedent(
            """\
            class Foo:
                @sngldsptchmthd
                def foo(self, a):
                    print(a)

                @foo.register
                def _(self: "Foo", a: list) -> None:
                    for idx, thing in enumerate(a):
                        print(idx, thing)
            """
        ),
        should_yield_error=False,
        dispatch_decorators={"sngldsptchmthd"},
    ),
}
