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
        arg(argname="test_arg"),
        "<Argument: test_arg, Annotated: False>",
        "Argument('test_arg', 0, 0, AnnotationType.ARGS, False, False, False)",
    ),
    "func_no_args": FormatTestCase(
        func(args=[arg(argname="return")]),
        "<Function: test_func, Args: [<Argument: return, Annotated: False>]>",
        (
            "Function('test_func', 0, 0, FunctionType.PUBLIC, False, None, False, False, "
            "[Argument('return', 0, 0, AnnotationType.ARGS, False, False, False)])"
        ),
    ),
    "func_has_arg": FormatTestCase(
        func(args=[arg(argname="foo"), arg(argname="return")]),
        "<Function: test_func, Args: [<Argument: foo, Annotated: False>, <Argument: return, Annotated: False>]>",  # noqa: E501
        (
            "Function('test_func', 0, 0, FunctionType.PUBLIC, False, None, False, False, "
            "[Argument('foo', 0, 0, AnnotationType.ARGS, False, False, False), "
            "Argument('return', 0, 0, AnnotationType.ARGS, False, False, False)])"
        ),
    ),
}
