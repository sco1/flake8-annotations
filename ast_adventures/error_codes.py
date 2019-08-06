from ast_adventures import Argument


class Error:
    """Represent linting error codes & relevant metadata."""

    def __init__(self, error_id: str, message: str):
        self.error_id = error_id
        self.message = message
        self.argname: str
        self.lineno: int
        self.col_offset: int

    def from_argument(self, argument: Argument):
        """Set error metadata from the input Argument object."""
        self.argname = argument.argname
        self.lineno = argument.lineno
        self.col_offset = argument.col_offset


# Function Annotations
TYP001 = Error("TYP001", "Missing type annotation for function argument")
TYP002 = Error("TYP002", "Missing type annotation for *args")
TYP003 = Error("TYP003", "Missing type annotation for **kwargs")

# Method Annotations
TYP101 = Error("TYP101", "Missing type annotation for self in class method")
TYP102 = Error("TYP102", "Missing type annotation for cls in classmethod")

# Return Annotations
TYP201 = Error("TYP201", "Missing return type annotation for public function")
TYP202 = Error("TYP202", "Missing return type annotation for protected function")
TYP203 = Error("TYP203", "Missing return type annotation for secret function")
TYP204 = Error("TYP204", "Missing return type annotation for magic function")
TYP205 = Error("TYP205", "Missing return type annotation for staticmethod")
TYP206 = Error("TYP206", "Missing return type annotation for classmethod")
