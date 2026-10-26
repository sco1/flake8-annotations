from textwrap import dedent

from testing.helpers import check_source, simplify_errors

SAMPLE_SRC = dedent("""\
    def bar(a):  # type: ignore
        ...

    def foo(  # type: ignore
        a,
    ):
        ...
    """)


def test_respect_type_ignore() -> None:
    # First check that we get errors from the source before we see if the flag has an effect
    yielded_errs = list(check_source(SAMPLE_SRC))
    assert yielded_errs

    errs = check_source(SAMPLE_SRC, respect_type_ignore=True)
    assert len(list(errs)) == 0


SAMPLE_TOP_LEVEL_MYPY_IGNORE = dedent("""\
    # mypy: ignore-errors

    def bar(a):
        ...
    """)


def test_respect_module_level_mypy_ignore() -> None:
    # First check that we get errors from the source before we see if the flag has an effect
    yielded_errs = list(check_source(SAMPLE_TOP_LEVEL_MYPY_IGNORE))
    assert yielded_errs

    errs = check_source(SAMPLE_TOP_LEVEL_MYPY_IGNORE, respect_type_ignore=True)
    assert len(list(errs)) == 0


SAMPLE_TOP_LEVEL_IGNORE = dedent("""\
    # type: ignore

    def bar(a):
        ...
    """)


def test_respect_module_level_type_ignore() -> None:
    # First check that we get errors from the source before we see if the flag has an effect
    yielded_errs = list(check_source(SAMPLE_TOP_LEVEL_IGNORE))
    assert yielded_errs

    errs = check_source(SAMPLE_TOP_LEVEL_IGNORE, respect_type_ignore=True)
    assert len(list(errs)) == 0


SAMPLE_FUNCTION_LEVEL_IGNORE = dedent("""\
    def foo(a):
        ...

    def bar(b):  # type: ignore
        ...
    """)


def test_respect_function_level_type_ignore() -> None:
    errs = check_source(SAMPLE_FUNCTION_LEVEL_IGNORE, respect_type_ignore=True)
    assert simplify_errors(errs) == [(1, "ANN001"), (1, "ANN201")]


SAMPLE_LINE_ONE_FUNCTION_LEVEL_IGNORE = dedent("""\
    def foo(a):  # type: ignore
        ...

    def bar(b):
        ...
    """)


def test_line_one_function_level_type_ignore() -> None:
    errs = check_source(SAMPLE_LINE_ONE_FUNCTION_LEVEL_IGNORE, respect_type_ignore=True)
    assert simplify_errors(errs) == [(4, "ANN001"), (4, "ANN201")]


SAMPLE_LINE_ONE_DECORATOR_IGNORE = dedent("""\
    @decorator  # type: ignore
    def foo(a):
        ...

    def bar(b):
        ...
    """)


def test_line_one_decorator_type_ignore() -> None:
    errs = check_source(SAMPLE_LINE_ONE_DECORATOR_IGNORE, respect_type_ignore=True)
    assert simplify_errors(errs) == [(2, "ANN001"), (2, "ANN201"), (5, "ANN001"), (5, "ANN201")]


SAMPLE_LINE_ONE_TRAILING_MYPY_IGNORE = dedent("""\
    def foo(a):  # mypy: ignore-errors
        ...

    def bar(b):
        ...
    """)


def test_line_one_trailing_mypy_ignore() -> None:
    errs = check_source(SAMPLE_LINE_ONE_TRAILING_MYPY_IGNORE, respect_type_ignore=True)
    assert simplify_errors(errs) == [(1, "ANN001"), (1, "ANN201"), (4, "ANN001"), (4, "ANN201")]
