from flake8_annotations import Argument
from flake8_annotations.enums import AnnotationType

# Build a dictionary of Argument objects corresponding to what we should be getting out of the
# argument parsing test
# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
parsed_arguments = {
    "all_args_untyped": [
        Argument(argname="arg", lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS),
        Argument(argname="vararg", lineno=0, col_offset=0, annotation_type=AnnotationType.VARARG),
        Argument(argname="kwonlyarg", lineno=0, col_offset=0, annotation_type=AnnotationType.KWONLYARGS),  # noqa
        Argument(argname="kwarg", lineno=0, col_offset=0, annotation_type=AnnotationType.KWARG),
        Argument(argname="return", lineno=0, col_offset=0, annotation_type=AnnotationType.RETURN),
    ],
    "all_args_typed": [
        Argument(
            argname="arg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.ARGS,
            has_type_annotation=True,
        ),
        Argument(
            argname="vararg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.VARARG,
            has_type_annotation=True,
        ),
        Argument(
            argname="kwonlyarg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.KWONLYARGS,
            has_type_annotation=True,
        ),
        Argument(
            argname="kwarg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.KWARG,
            has_type_annotation=True,
        ),
        Argument(
            argname="return",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.RETURN,
            has_type_annotation=True,
        ),
    ],
}
