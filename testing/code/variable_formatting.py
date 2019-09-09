"""
Check for successful substitution of variable name into error codes.

Current substituting error codes:
  TYP001 Missing type annotation for function argument '{}'
  TYP002 Missing type annotation for *{}
  TYP003 Missing type annotation for **{}

This test should yield 48 linting errors (3 per function for 16 functions)
"""


def foo(some_arg, *some_args, **some_kwargs) -> int:
    pass


def _foo(some_arg, *some_args, **some_kwargs) -> int:
    pass


def __foo(some_arg, *some_args, **some_kwargs) -> int:
    pass


def __foo__(some_arg, *some_args, **some_kwargs) -> int:
    pass


# Class methods
class Snek:
    def foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    def _foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    def __foo(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    def __foo__(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    @classmethod
    def bar(cls: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    @classmethod
    def _bar(cls: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    @classmethod
    def __bar(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    @classmethod
    def __bar__(self: Snek, some_arg, *some_args, **some_kwargs) -> int:
        pass

    @staticmethod
    def baz(some_arg, *some_args, **some_kwargs) -> int:
        pass

    @staticmethod
    def _baz(some_arg, *some_args, **some_kwargs) -> int:
        pass

    @staticmethod
    def __baz(some_arg, *some_args, **some_kwargs) -> int:
        pass

    @staticmethod
    def __baz__(some_arg, *some_args, **some_kwargs) -> int:
        pass
