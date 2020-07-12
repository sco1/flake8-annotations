from textwrap import dedent
from typing import NamedTuple


class MypyInitReturnTestCase(NamedTuple):
    """
    Helper container for testing mypy-style omission of __init__ return hints.

    Mypy allows the omission of return type hints if at least one argument is annotated.
    """

    src: str
    should_yield_return_error: bool


mypy_init_test_cases = {
    "no_args_no_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self):
                    ...
            """
        ),
        should_yield_return_error=True,
    ),
    "arg_no_hint_no_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self, foo):
                    ...
            """
        ),
        should_yield_return_error=True,
    ),
    "arg_no_hint_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self, foo) -> None:
                    ...
            """
        ),
        should_yield_return_error=False,
    ),
    "no_arg_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self) -> None:
                    ...
            """
        ),
        should_yield_return_error=False,
    ),
    "arg_hint_no_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self, foo: int):
                    ...
            """
        ),
        should_yield_return_error=False,
    ),
    "arg_hint_return": MypyInitReturnTestCase(
        src=dedent(
            """\
            class Foo:

                def __init__(self, foo: int) -> None:
                    ...
            """
        ),
        should_yield_return_error=False,
    ),
    "cheeky_non_method_init": MypyInitReturnTestCase(
        src=dedent(
            """\
            def __init__(self, foo: int):
                ...
            """
        ),
        should_yield_return_error=True,
    ),
}
