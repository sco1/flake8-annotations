from textwrap import dedent
from typing import NamedTuple, Tuple


class ParserTestCase(NamedTuple):
    """
    Helper container for line & column number test cases.

    Error locations are provided as a tuple of (row number, column offset) tuples
        * Row numbers are 1-indexed
        * Column offsets are 0-indexed when yielded by our checker; flake8 adds 1 when emitted
    """

    src: str
    error_locations: Tuple[Tuple[int, int], ...]


parser_test_cases = {
    "undecorated_def": ParserTestCase(
        src=dedent(
            """\
            def bar(x):  # 1
                pass     # 2
            """
        ),
        error_locations=(
            (1, 8),
            (1, 10),
        ),
    ),
    "decorated_def": ParserTestCase(
        src=dedent(
            """\
            @property              # 1
            @some_decorator        # 2
            @some_other_decorator  # 3
            def foo(               # 4
                x,                 # 5
                y,                 # 6
            ):                     # 7
                pass               # 8
            """
        ),
        error_locations=(
            (5, 4),
            (6, 4),
            (7, 1),
        ),
    ),
    "single_line_docstring": ParserTestCase(
        src=dedent(
            """\
            def baz():                    # 1
                \"\"\"A docstring.\"\"\"  # 2
                pass                      # 3
            """
        ),
        error_locations=((1, 9),),
    ),
    "multiline_docstring": ParserTestCase(
        src=dedent(
            """\
            def snek():              # 1
                \"\"\"               # 2
                Some.                # 3
                                     # 4
                Multiline docstring  # 5
                \"\"\"               # 6
                pass                 # 7
            """
        ),
        error_locations=((1, 10),),
    ),
    "hinted_arg": ParserTestCase(
        src=dedent(
            """\
            def foo(bar: bool):  # 1
                return True      # 2
            """
        ),
        error_locations=((1, 18),),
    ),
    "docstring_with_colon": ParserTestCase(
        src=dedent(
            """\
            def baz():                     # 1
                \"\"\"A: docstring.\"\"\"  # 2
                pass                       # 3
            """
        ),
        error_locations=((1, 9),),
    ),
    "multiline_docstring_with_colon": ParserTestCase(
        src=dedent(
            """\
            def snek():               # 1
                \"\"\"                # 2
                Some.                 # 3
                                      # 4
                Multiline: docstring  # 5
                \"\"\"                # 6
                pass                  # 7
            """
        ),
        error_locations=((1, 10),),
    ),
    "single_line_def": ParserTestCase(
        src=dedent(
            """\
            def lol(): \"\"\"Some docstring.\"\"\"  # 1
            """
        ),
        error_locations=((1, 9),),
    ),
    "single_line_def_docstring_with_colon": ParserTestCase(
        src=dedent(
            """\
            def lol(): \"\"\"Some: docstring.\"\"\"  # 1
            """
        ),
        error_locations=((1, 9),),
    ),
    "single_line_hinted_def": ParserTestCase(
        src=dedent(
            """\
            def lol(x: int): \"\"\"Some: docstring.\"\"\"  # 1
            """
        ),
        error_locations=((1, 15),),
    ),
    "multiline_docstring_no_content": ParserTestCase(
        src=dedent(
            """\
            def foo():  # 1
                \"\"\"  # 2
                \"\"\"  # 3
                ...     # 4
            """
        ),
        error_locations=((1, 9),),
    ),
    "multiline_docstring_summary_at_open": ParserTestCase(
        src=dedent(
            """\
            def foo():                 # 1
                \"\"\"Some docstring.  # 2
                \"\"\"                 # 3
                ...                    # 4
            """
        ),
        error_locations=((1, 9),),
    ),
    "multiline_docstring_single_line_summary": ParserTestCase(
        src=dedent(
            """\
            def foo():           # 1
                \"\"\"           # 2
                Some docstring.  # 3
                \"\"\"           # 4
                ...              # 5
            """
        ),
        error_locations=((1, 9),),
    ),
}
