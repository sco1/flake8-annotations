from functools import partial

from flake8_annotations import Argument
from flake8_annotations.enums import AnnotationType

untyped_arg = partial(
    Argument, lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS, has_type_annotation=False
)
typed_arg = partial(
    Argument, lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS, has_type_annotation=True
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
}
