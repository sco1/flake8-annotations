from textwrap import dedent
from typing import NamedTuple


class TypeCommentArgInjectTestCase(NamedTuple):
    """Helper container for tests for the injection of `self` or `cls` intoto class methods."""

    src: str
    should_yield_ANN100: bool


type_comment_arg_inject_test_cases = {
    "untyped_self_arg": TypeCommentArgInjectTestCase(
        src=dedent(
            """\
            class Foo:

                def bar(self, a):
                    # type: (bool) -> float
                    ...
            """
        ),
        should_yield_ANN100=True,
    ),
    "untyped_cls_arg": TypeCommentArgInjectTestCase(
        src=dedent(
            """\
            class Foo:

                @classmethod
                def bar(cls, a):
                    # type: (bool) -> float
                    ...
            """
        ),
        should_yield_ANN100=True,
    ),
    "untyped_staticmethod": TypeCommentArgInjectTestCase(
        src=dedent(
            """\
            class Foo:

                @staticmethod
                def bar(a):
                    # type: (...) -> float
                    ...
            """
        ),
        should_yield_ANN100=False,
    ),
    "typed_self_arg": TypeCommentArgInjectTestCase(
        src=dedent(
            """\
            class Foo:

                def bar(self, a):
                    # type: ("Foo", bool) -> float
                    ...
            """
        ),
        should_yield_ANN100=False,
    ),
    "typed_cls_arg": TypeCommentArgInjectTestCase(
        src=dedent(
            """\
            class Foo:

                @classmethod
                def bar(cls, a):
                    # type: ("Foo", bool) -> float
                    ...
            """
        ),
        should_yield_ANN100=False,
    ),
}
