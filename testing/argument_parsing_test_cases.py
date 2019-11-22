from functools import partial
from textwrap import dedent
from typing import NamedTuple, Tuple

from flake8_annotations import Argument
from flake8_annotations.enums import AnnotationType


class ArgumentTestCase(NamedTuple):
    """Helper container for Argument parsing test cases."""

    src: str
    args: Tuple[Argument]


# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
# using partial objects
untyped_arg = partial(Argument, lineno=0, col_offset=0, has_type_annotation=False)
typed_arg = partial(
    Argument, lineno=0, col_offset=0, has_type_annotation=True, has_3107_annotation=True
)

argument_test_cases = {
    "all_args_untyped": ArgumentTestCase(
        src=dedent(
            """\
            def all_args_untyped(arg, *vararg, kwonlyarg, **kwarg):
                pass
            """
        ),
        args=(
            untyped_arg(argname="arg", annotation_type=AnnotationType.ARGS),
            untyped_arg(argname="vararg", annotation_type=AnnotationType.VARARG),
            untyped_arg(argname="kwonlyarg", annotation_type=AnnotationType.KWONLYARGS),
            untyped_arg(argname="kwarg", annotation_type=AnnotationType.KWARG),
            untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ),
    ),
    "all_args_typed": ArgumentTestCase(
        src=dedent(
            """\
            def all_args_typed(arg: int, *vararg: int, kwonlyarg: int, **kwarg: int) -> int:
                pass
            """
        ),
        args=(
            typed_arg(argname="arg", annotation_type=AnnotationType.ARGS),
            typed_arg(argname="vararg", annotation_type=AnnotationType.VARARG),
            typed_arg(argname="kwonlyarg", annotation_type=AnnotationType.KWONLYARGS),
            typed_arg(argname="kwarg", annotation_type=AnnotationType.KWARG),
            typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ),
    ),
}  # TODO: Add POSONLYARG case
