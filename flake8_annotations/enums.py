from enum import Enum, auto


class FunctionType(Enum):
    """
    Represent Python's function types.

    Note: while Python differentiates between a function and a method, for the purposes of this
    tool, both will be referred to as functions outside of any class-specific context. This also
    aligns with ast's naming convention.
    """

    PUBLIC = auto()
    PROTECTED = auto()  # Leading single underscore
    PRIVATE = auto()  # Leading double underscore
    SPECIAL = auto()  # Leading & trailing double underscore


class ClassDecoratorType(Enum):
    """Represent Python's built-in class method decorators."""

    CLASSMETHOD = auto()
    STATICMETHOD = auto()


class AnnotationType(Enum):
    """Represent the kind of missing type annotation."""

    POSONLYARGS = auto()
    ARGS = auto()
    VARARG = auto()
    KWONLYARGS = auto()
    KWARG = auto()
    RETURN = auto()
