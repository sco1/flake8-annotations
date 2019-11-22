from textwrap import dedent
from typing import NamedTuple


class AnnotationTestCase(NamedTuple):
    """Helper container for annotation presence test cases."""

    src: str
    is_fully_annotated: bool


annotation_test_cases = {
    "no_arg_no_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo(a, b):
                pass
            """
        ),
        is_fully_annotated=False,
    ),
    "partial_arg_no_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo(a: int, b):
                pass
            """
        ),
        is_fully_annotated=False,
    ),
    "partial_arg_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo(a: int, b) -> int:
                pass
            """
        ),
        is_fully_annotated=False,
    ),
    "full_args_no_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo(a: int, b: int):
                pass
            """
        ),
        is_fully_annotated=False,
    ),
    "no_args_no_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo():
                pass
            """
        ),
        is_fully_annotated=False,
    ),
    "full_arg_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo(a: int, b: int) -> int:
                pass
            """
        ),
        is_fully_annotated=True,
    ),
    "no_args_return": AnnotationTestCase(
        src=dedent(
            """\
            def foo() -> int:
                pass
            """
        ),
        is_fully_annotated=True,
    ),
}
