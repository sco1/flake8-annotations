from __future__ import annotations

import typing as t

from flake8_annotations import checker

if t.TYPE_CHECKING:
    from flake8_annotations.ast_walker import Argument, Function


class Error:
    """
    Represent linting error codes & relevant metadata.

    This is not designed to be instantiated directly, instead providing common methods to reduce
    copypasta when defining new error codes. New error codes should inherit this class & accept the
    `argname`, `lineno`, and `col_offset` parameters; the error `message` should be constant for
    each error code.
    """

    argname: str
    lineno: int
    col_offset: int

    def __init__(self, message: str):
        self.message = message

    @classmethod
    def from_argument(cls, argument: Argument) -> Error:
        """Set error metadata from the input Argument object."""
        return cls(argument.argname, argument.lineno, argument.col_offset)  # type: ignore[call-arg]

    @classmethod
    def from_function(cls, function: Function) -> Error:
        """Set error metadata from the input Function object."""
        return cls(function.name, function.lineno, function.col_offset)  # type: ignore[call-arg]

    def to_flake8(self) -> t.Tuple[int, int, str, t.Type[t.Any]]:
        """
        Format the Error into what Flake8 is expecting.

        Expected output is a tuple with the following information:
          (line number, column number, message, checker type)
        """
        return (self.lineno, self.col_offset, self.message, checker.TypeHintChecker)


# Function Annotations
class ANN001(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN001 Missing type annotation for function argument '{}'")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> t.Tuple[int, int, str, t.Type[t.Any]]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


class ANN002(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN002 Missing type annotation for *{}")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> t.Tuple[int, int, str, t.Type[t.Any]]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


class ANN003(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN003 Missing type annotation for **{}")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> t.Tuple[int, int, str, t.Type[t.Any]]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


# Method annotations
class ANN101(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN101 Missing type annotation for self in method")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN102(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN102 Missing type annotation for cls in classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Return annotations
class ANN201(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN201 Missing return type annotation for public function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN202(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN202 Missing return type annotation for protected function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN203(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN203 Missing return type annotation for secret function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN204(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN204 Missing return type annotation for special method")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN205(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN205 Missing return type annotation for staticmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class ANN206(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN206 Missing return type annotation for classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Type comments
class ANN301(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN301 PEP 484 disallows both type annotations and type comments")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Opinionated warnings
class ANN401(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("ANN401 Dynamically typed expressions (typing.Any) are disallowed")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
