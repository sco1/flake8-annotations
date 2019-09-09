"""
Check for column offset & line number correctness.

Should yield:

20:9: TYP001 Missing type annotation for function argument 'x'
20:12: TYP201 Missing return type annotation for public function
28:5: TYP001 Missing type annotation for function argument 'x'
29:5: TYP001 Missing type annotation for function argument 'y'
30:3: TYP201 Missing return type annotation for public function
34:10: TYP201 Missing return type annotation for public function
39:11: TYP201 Missing return type annotation for public function

Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
Note: Column offsets and line numbers are hard-coded in the testing suite, ensure these are updated
      appropriately (location & order) if any changes are made to this source code.
"""


def bar(x):
    pass


@property
@some_decorator
@some_other_decorator
def foo(
    x,
    y
):
    pass


def baz():
    """A docstring."""
    pass


def snek():
    """
    Some.

    Multiline docstring
    """
    pass
