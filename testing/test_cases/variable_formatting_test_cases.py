from textwrap import dedent
from typing import NamedTuple


class FormatTestCase(NamedTuple):
    """Helper container for variable formatting test cases."""

    src: str


variable_formatting_test_cases = {
    "public_function": FormatTestCase(
        src=dedent(
            """\
            def foo(some_arg, *some_args, **some_kwargs) -> int:
                pass
            """
        ),
    ),
    "protected_function": FormatTestCase(
        src=dedent(
            """\
            def _foo(some_arg, *some_args, **some_kwargs) -> int:
                pass
            """
        ),
    ),
    "private_function": FormatTestCase(
        src=dedent(
            """\
            def __foo(some_arg, *some_args, **some_kwargs) -> int:
                pass
            """
        ),
    ),
    "special_function": FormatTestCase(
        src=dedent(
            """\
            def __foo__(some_arg, *some_args, **some_kwargs) -> int:
                pass
            """
        ),
    ),
    "class_method": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                def foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "protected_class_method": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                def _foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "private_class_method": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                def __foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "magic_class_method": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                def __foo__(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "public_classmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @classmethod
                def bar(cls: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "protected_classmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @classmethod
                def _bar(cls: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "private_classmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @classmethod
                def __bar(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "magic_classmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @classmethod
                def __bar__(cls: Snek, some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "public_staticmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @staticmethod
                def baz(some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "protected_staticmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @staticmethod
                def _baz(some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "private_staticmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @staticmethod
                def __baz(some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
    "magic_staticmethod": FormatTestCase(
        src=dedent(
            """\
            class Snek:
                @staticmethod
                def __baz__(some_arg, *some_args, **some_kwargs) -> int:
                    pass
            """
        ),
    ),
}
