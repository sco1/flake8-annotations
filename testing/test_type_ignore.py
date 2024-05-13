from textwrap import dedent

from testing.helpers import check_source

SAMPLE_SRC = dedent(
    """\
    def bar(a):  # type: ignore
        ...

    def foo(  # type: ignore
        a,
    ):
        ...
    """
)


def test_respect_type_ignore() -> None:
    errs = check_source(SAMPLE_SRC, respect_type_ignore=True)
    assert len(list(errs)) == 0


SAMPLE_TOP_LEVEL_MYPY_IGNORE = dedent(
    """\
    # mypy: ignore-errors

    def bar(a):
        ...
    """
)


def test_respect_module_level_mypy_ignore() -> None:
    errs = check_source(SAMPLE_TOP_LEVEL_MYPY_IGNORE, respect_type_ignore=True)
    assert len(list(errs)) == 0


SAMPLE_TOP_LEVEL_IGNORE = dedent(
    """\
    # type: ignore

    def bar(a):
        ...
    """
)


def test_respect_module_level_type_ignore() -> None:
    errs = check_source(SAMPLE_TOP_LEVEL_IGNORE, respect_type_ignore=True)
    assert len(list(errs)) == 0
