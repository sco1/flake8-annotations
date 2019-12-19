from subprocess import PIPE, run


def test_checker_runs() -> None:
    """Test that the checker is properly registered by Flake8 as needing to run on the input src."""
    substr = "TYP001 Missing type annotation for function argument 'x'"
    p = run(["flake8", "-"], stdout=PIPE, input="def bar(x) -> None:\n    pass\n", encoding="ascii")

    assert substr in p.stdout
