from functools import partial
from typing import NamedTuple, Union

from flake8_annotations.ast_walker import Argument, Function
from flake8_annotations.enums import AnnotationType


class FormatTestCase(NamedTuple):
    """Named tuple for representing our test cases."""

    test_object: Union[Argument, Function]
    str_output: str


# Define partial functions to simplify object creation
arg = partial(Argument, lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS)
func = partial(Function, name="test_func", lineno=0, col_offset=0, decorator_list=[])

formatting_test_cases = {
    "arg": FormatTestCase(
        test_object=arg(argname="test_arg"),
        str_output="<Argument: test_arg, Annotated: False>",
    ),
    "func_no_args": FormatTestCase(
        test_object=func(args=[arg(argname="return")]),
        str_output="<Function: test_func, Args: [<Argument: return, Annotated: False>]>",
    ),
    "func_has_arg": FormatTestCase(
        test_object=func(args=[arg(argname="foo"), arg(argname="return")]),
        str_output="<Function: test_func, Args: [<Argument: foo, Annotated: False>, <Argument: return, Annotated: False>]>",
    ),
}
