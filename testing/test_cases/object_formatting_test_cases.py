from functools import partial
from typing import NamedTuple, Union

from flake8_annotations import Argument, Function
from flake8_annotations.enums import AnnotationType


class FormatTestCase(NamedTuple):
    """Named tuple for representing our test cases."""

    test_object: Union[Argument, Function]
    str_output: str
    repr_output: str


# Define partial functions to simplify object creation
arg = partial(Argument, lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS)
func = partial(Function, name="test_func", lineno=0, col_offset=0)

formatting_test_cases = {
    "arg": FormatTestCase(
        test_object=arg(argname="test_arg"),
        str_output="<Argument: test_arg, Annotated: False>",
        repr_output=(
            "Argument("
            "argname='test_arg', "
            "lineno=0, "
            "col_offset=0, "
            "annotation_type=AnnotationType.ARGS, "
            "has_type_annotation=False, "
            "has_3107_annotation=False, "
            "has_type_comment=False"
            ")"
        ),
    ),
    "func_no_args": FormatTestCase(
        test_object=func(args=[arg(argname="return")]),
        str_output="<Function: test_func, Args: [<Argument: return, Annotated: False>]>",
        repr_output=(
            "Function("
            "name='test_func', "
            "lineno=0, "
            "col_offset=0, "
            "function_type=FunctionType.PUBLIC, "
            "is_class_method=False, "
            "class_decorator_type=None, "
            "is_return_annotated=False, "
            "has_type_comment=False, "
            "has_only_none_returns=True, "
            "is_overload_decorated=False, "
            "args=[Argument(argname='return', lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS, "  # noqa: E501
            "has_type_annotation=False, has_3107_annotation=False, has_type_comment=False)]"
            ")"
        ),
    ),
    "func_has_arg": FormatTestCase(
        test_object=func(args=[arg(argname="foo"), arg(argname="return")]),
        str_output="<Function: test_func, Args: [<Argument: foo, Annotated: False>, <Argument: return, Annotated: False>]>",  # noqa: E501
        repr_output=(
            "Function("
            "name='test_func', "
            "lineno=0, "
            "col_offset=0, "
            "function_type=FunctionType.PUBLIC, "
            "is_class_method=False, "
            "class_decorator_type=None, "
            "is_return_annotated=False, "
            "has_type_comment=False, "
            "has_only_none_returns=True, "
            "is_overload_decorated=False, "
            "args=[Argument(argname='foo', lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS, "  # noqa: E501
            "has_type_annotation=False, has_3107_annotation=False, has_type_comment=False), "
            "Argument(argname='return', lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS, "  # noqa: E501
            "has_type_annotation=False, has_3107_annotation=False, has_type_comment=False)]"
            ")"
        ),
    ),
}
