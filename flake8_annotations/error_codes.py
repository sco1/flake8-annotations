from typing import Tuple, Type

from flake8_annotations import Argument, Function, checker


class Error:
    """Represent linting error codes & relevant metadata."""

    def __init__(self, message: str):
        self.message = message
        self.argname: str
        self.lineno: int
        self.col_offset: int

    @classmethod
    def from_argument(cls, argument: Argument):
        """Set error metadata from the input Argument object."""
        return cls(argument.argname, argument.lineno, argument.col_offset)

    @classmethod
    def from_function(cls, function: Function):
        """Set error metadata from the input Function object."""
        return cls(function.name, function.lineno, function.col_offset)

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """
        Format the Error into what Flake8 is expecting.

        Expected output is a tuple with the following information:
          (line number, column number, message, checker type)
        """
        return (self.lineno, self.col_offset, self.message, checker.TypeHintChecker)


# Function Annotations
class TYP001(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP001 Missing type annotation for function argument '{}'")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


class TYP002(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP002 Missing type annotation for *{}")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


class TYP003(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP003 Missing type annotation for **{}")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """Overload super's formatter so we can include argname in the output."""
        return (
            self.lineno,
            self.col_offset,
            self.message.format(self.argname),
            checker.TypeHintChecker,
        )


# Method annotations
class TYP101(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP101 Missing type annotation for self in method")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP102(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP102 Missing type annotation for cls in classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Return annotations
class TYP201(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP201 Missing return type annotation for public function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP202(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP202 Missing return type annotation for protected function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP203(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP203 Missing return type annotation for secret function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP204(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP204 Missing return type annotation for special method")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP205(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP205 Missing return type annotation for staticmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP206(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP206 Missing return type annotation for classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Type comments
class TYP301(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP301 PEP 484 disallows both type annotations and type comments")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
