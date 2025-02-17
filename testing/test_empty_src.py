from testing.helpers import check_source

def test_empty_source() -> None:
    # Existing test: empty source should yield no errors.
    errs = check_source("")
    assert len(list(errs)) == 0

def test_whitespace_source() -> None:
    # Test that a source with only whitespace returns no errors.
    src = "   \n   \n  "
    errs = check_source(src)
    assert len(list(errs)) == 0

def test_comment_only_source() -> None:
    # Test that a source with only comments returns no errors.
    src = "# This is a comment\n# Another comment"
    errs = check_source(src)
    assert len(list(errs)) == 0
