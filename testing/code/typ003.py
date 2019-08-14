"""
Check for TYP003: Missing type annotation for **kwargs.

Should yield:

10:30: TYP003 Missing type annotation for **kwargs
19:5: TYP003 Missing type annotation for **kwargs
"""

def foo(a: int, *args: List, **kwargs) -> None:
    pass

def bar(a: int, *args: List, **kwargs: Dict) -> None:
    pass

def baz(
    a: int,
    *args: List,
    **kwargs
) -> None:
    pass

def snek(
    a: int,
    *args: List,
    **kwargs: Dict
) -> None:
    pass
