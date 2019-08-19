"""Check for correct parsing of argument types & type annotation presence."""


def all_args_untyped(arg, *vararg, kwonlyarg, **kwarg):
    pass


def all_args_typed(arg: int, *vararg: int, kwonlyarg: int, **kwarg: int) -> int:
    pass
