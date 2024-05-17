from testing.helpers import check_source


def test_empty_source() -> None:
    errs = check_source("")
    assert len(list(errs)) == 0
