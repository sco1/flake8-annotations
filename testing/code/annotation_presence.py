"""
Check for correct determination that the function is or isn't fully annotated.

Note: Function definitions & the truth value for Function.is_fully_annotated are hardcoded in the
test. Ensure these are updated if this source code changes.
"""


# Should return False
def no_arg_no_return(a, b):
    pass


def partial_arg_no_return(a: int, b):
    pass


def partial_arg_return(a: int, b) -> int:
    pass


def full_args_no_return(a: int, b: int):
    pass


def no_args_no_return():
    pass


# Should return True
def full_arg_return(a: int, b: int) -> int:
    pass


def no_args_return() -> int:
    pass
