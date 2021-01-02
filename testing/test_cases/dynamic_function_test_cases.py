from textwrap import dedent
from typing import NamedTuple


class DynamicallyTypedFunctionTestCase(NamedTuple):
    """Container for tests for the suppression of errors for dynamically typed functions."""

    src: str
    should_yield_error: bool


dynamic_function_test_cases = {
    "def_no_hints": DynamicallyTypedFunctionTestCase(
        src=dedent(
            """\
            def foo(a):
                b = a + 2
            """
        ),
        should_yield_error=False,
    ),
    "def_has_return_hint": DynamicallyTypedFunctionTestCase(
        src=dedent(
            """\
            def foo(a) -> None:
                b = a + 2
            """
        ),
        should_yield_error=True,
    ),
    "class_init_no_hints": DynamicallyTypedFunctionTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self):
                    self.a = "Hello World"
            """
        ),
        should_yield_error=False,
    ),
    "typed_class_init_no_return_hint": DynamicallyTypedFunctionTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self: "Foo", a: str):
                    self.a = a
            """
        ),
        should_yield_error=True,
    ),
}


class DynamicallyTypedNestedFunctionTestCase(NamedTuple):
    """Container for tests for the suppression of errors for dynamically typed nested functions."""

    src: str
    should_yield_error: bool


nested_dynamic_function_test_cases = {
    "def_no_hints": DynamicallyTypedNestedFunctionTestCase(
        src=dedent(
            """\
            def foo(a):
                b = a + 2
            """
        ),
        should_yield_error=True,
    ),
    "class_init_no_hints": DynamicallyTypedNestedFunctionTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self):
                    self.a = "Hello World"
            """
        ),
        should_yield_error=True,
    ),
    "nested_def_partial_hints": DynamicallyTypedNestedFunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar(a: int):
                    b = a + 2
            """
        ),
        should_yield_error=True,
    ),
    "nested_def_no_hints": DynamicallyTypedNestedFunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar(a):
                    b = a + 2
            """
        ),
        should_yield_error=False,
    ),
    "double_nested_def_no_hints": DynamicallyTypedNestedFunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar() -> None:
                    def baz(a):
                        b = a + 2
            """
        ),
        should_yield_error=False,
    ),
}
