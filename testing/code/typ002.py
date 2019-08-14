"""
Check for TYP002: Missing type annotation for *args.

Should yield:

10:17: TYP002 Missing type annotation for *args
18:5: TYP002 Missing type annotation for *args
"""

def foo(a: int, *args) -> None:
    pass

def bar(a: int, *args: List) -> None:
    pass

def baz(
    a: int,
    *args
) -> None:
    pass

def snek(
    a: int,
    *args: List
) -> None:
    pass
