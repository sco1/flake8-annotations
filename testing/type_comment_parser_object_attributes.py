from functools import partial

from flake8_annotations import Argument
from flake8_annotations.enums import AnnotationType

untyped_arg = partial(
    Argument,
    lineno=0,
    col_offset=0,
    annotation_type=AnnotationType.ARGS,
    has_type_annotation=False,
    has_type_comment=False,
    has_3107_annotation=False,
)
typed_arg = partial(
    Argument,
    lineno=0,
    col_offset=0,
    annotation_type=AnnotationType.ARGS,
    has_type_annotation=True,
    has_type_comment=True,
    has_3107_annotation=False,
)

parsed_arguments = {
    "full_function_comment": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2"),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "partial_function_comment_no_ellipsis": [
        typed_arg(argname="arg1"),
        untyped_arg(argname="arg2"),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "partial_function_comment_with_ellipsis": [
        untyped_arg(argname="arg1"),
        typed_arg(argname="arg2"),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "argument_comments_ellipsis_function_comment": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2"),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "argument_comments_no_function_comment": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2"),
        untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "mixed_argument_hint_types": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2", has_type_comment=False, has_3107_annotation=True),
        untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "duplicate_argument_hint_types": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2", has_type_comment=True, has_3107_annotation=True),
        untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "arg_comment_return_annotation_hint_types": [
        typed_arg(argname="arg1"),
        typed_arg(argname="arg2"),
        typed_arg(
            argname="return",
            annotation_type=AnnotationType.RETURN,
            has_type_comment=False,
            has_3107_annotation=True,
        ),
    ],
    "arg_annotation_return_comment_hint_types": [
        typed_arg(argname="arg1", has_type_comment=False, has_3107_annotation=True),
        typed_arg(argname="arg2", has_type_comment=False, has_3107_annotation=True),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN, has_type_comment=True),
    ],
}
