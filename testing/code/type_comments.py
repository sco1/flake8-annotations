"""Check for correct parsing of PEP 484-style type comments."""


def full_function_comment(arg1, arg2):
    # type: (int, int) -> int
    pass


def partial_function_comment_no_ellipsis(arg1, arg2):
    # type: (int) -> int
    pass


def partial_function_comment_with_ellipsis(arg1, arg2):
    # type: (..., int) -> int
    pass


def argument_comments_ellipsis_function_comment(
    arg1,  # type: int
    arg2,  # type: int
):  # type: (...) -> int
    pass


def argument_comments_no_function_comment(
    arg1,  # type: int
    arg2,  # type: int
):
    pass
