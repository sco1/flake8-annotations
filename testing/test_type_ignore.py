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
