"""
Check for TYP001: Missing type annotation for function argument.

Should yield:

10:9: TYP001 Missing type annotation for function argument 'a'
17:5: TYP001 Missing type annotation for function argument 'a'
"""

def foo(a) -> None:
    pass

def bar(a: int) -> None:
    pass

def baz(
    a
) -> None:
    pass

def snek(
    a: int
) -> None:
    pass