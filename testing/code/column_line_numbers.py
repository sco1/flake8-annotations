"""
Check for column offset & line number correctness.

Should Yield:

16:9: TYP001 Missing type annotation for function argument 'x'
16:12: TYP201 Missing return type annotation for public function
24:5: TYP001 Missing type annotation for function argument 'x'
25:5: TYP001 Missing type annotation for function argument 'y'
26:3: TYP201 Missing return type annotation for public function

Note: Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
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
