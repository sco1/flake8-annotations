import sys
from functools import partial
from typing import Iterable, List, Optional, Tuple

from flake8_annotations import Argument, Function
from flake8_annotations.enums import AnnotationType

if sys.version_info >= (3, 8):
    import ast

    PY_GTE_38 = True
else:
    from typed_ast import ast3 as ast

    PY_GTE_38 = False


def parse_source(src: str) -> Tuple[ast.Module, List[str]]:
    """Parse the provided Python source string and return an (typed AST, source) tuple."""
    if PY_GTE_38:
        # Built-in ast requires a flag to parse type comments
        tree = ast.parse(src, type_comments=True)
    else:
        # typed-ast will implicitly parse type comments
        tree = ast.parse(src)

    lines = src.splitlines()

    return tree, lines


def find_matching_function(func_list: Iterable[Function], match_name: str) -> Optional[Function]:
    """
    Iterate over a list of Function objects & find the matching named function.

    If no function is found, this returns None
    """
    for function in func_list:
        if function.name == match_name:
            return function


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
