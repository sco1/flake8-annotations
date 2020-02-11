from typing import NamedTuple

from flake8_annotations import error_codes
from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType


# Build a dictionary of possible function combinations & the resultant error code
# Keys are named tuples of the form (function_type, is_class_method, class_decorator_type)
class RT(NamedTuple):
    """Helper object for return type attribute specification."""

    function_type: FunctionType
    is_class_method: bool
    class_decorator_type: ClassDecoratorType


return_classifications = {
    # ANN206 Missing return type annotation for classmethod
    RT(FunctionType.PUBLIC, True, ClassDecoratorType.CLASSMETHOD): error_codes.ANN206,
    RT(FunctionType.PROTECTED, True, ClassDecoratorType.CLASSMETHOD): error_codes.ANN206,
    RT(FunctionType.PRIVATE, True, ClassDecoratorType.CLASSMETHOD): error_codes.ANN206,
    RT(FunctionType.SPECIAL, True, ClassDecoratorType.CLASSMETHOD): error_codes.ANN206,
    # ANN205 Missing return type annotation for staticmethod
    RT(FunctionType.PUBLIC, True, ClassDecoratorType.STATICMETHOD): error_codes.ANN205,
    RT(FunctionType.PROTECTED, True, ClassDecoratorType.STATICMETHOD): error_codes.ANN205,
    RT(FunctionType.PRIVATE, True, ClassDecoratorType.STATICMETHOD): error_codes.ANN205,
    RT(FunctionType.SPECIAL, True, ClassDecoratorType.STATICMETHOD): error_codes.ANN205,
    # ANN204 Missing return type annotation for special method
    RT(FunctionType.SPECIAL, True, None): error_codes.ANN204,
    RT(FunctionType.SPECIAL, False, None): error_codes.ANN204,
    # ANN203 Missing return type annotation for secret function
    RT(FunctionType.PRIVATE, True, None): error_codes.ANN203,
    RT(FunctionType.PRIVATE, False, None): error_codes.ANN203,
    # ANN202 Missing return type annotation for protected function
    RT(FunctionType.PROTECTED, True, None): error_codes.ANN202,
    RT(FunctionType.PROTECTED, False, None): error_codes.ANN202,
    # ANN201 Missing return type annotation for public function
    RT(FunctionType.PUBLIC, True, None): error_codes.ANN201,
    RT(FunctionType.PUBLIC, False, None): error_codes.ANN201,
}


# Build a dictionary of possible argument combinations & the resultant error code
# Keys are named tuples of the form:
#   (is_class_method, is_first_arg, class_decorator_type, annotation_type)
class AT(NamedTuple):
    """Helper object for return type attribute specification."""

    is_class_method: bool
    is_first_arg: bool
    class_decorator_type: ClassDecoratorType
    annotation_type: AnnotationType


argument_classifications = {
    # ANN102 Missing type annotation for cls in classmethod
    AT(True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.ARGS): error_codes.ANN102,
    AT(True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.VARARG): error_codes.ANN102,
    AT(True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWONLYARGS): error_codes.ANN102,
    AT(True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWARG): error_codes.ANN102,
    # ANN101 Missing type annotation for self in method
    AT(True, True, None, AnnotationType.ARGS): error_codes.ANN101,
    AT(True, True, None, AnnotationType.VARARG): error_codes.ANN101,
    AT(True, True, None, AnnotationType.KWONLYARGS): error_codes.ANN101,
    AT(True, True, None, AnnotationType.KWARG): error_codes.ANN101,
    # ANN003 Missing type annotation for **kwargs
    AT(True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWARG): error_codes.ANN003,
    AT(True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.KWARG): error_codes.ANN003,
    AT(True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.KWARG): error_codes.ANN003,
    AT(True, False, None, AnnotationType.KWARG): error_codes.ANN003,
    AT(False, True, None, AnnotationType.KWARG): error_codes.ANN003,
    AT(False, False, None, AnnotationType.KWARG): error_codes.ANN003,
    # ANN002 Missing type annotation for *args
    AT(True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.VARARG): error_codes.ANN002,
    AT(True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.VARARG): error_codes.ANN002,
    AT(True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.VARARG): error_codes.ANN002,
    AT(True, False, None, AnnotationType.VARARG): error_codes.ANN002,
    AT(False, True, None, AnnotationType.VARARG): error_codes.ANN002,
    AT(False, False, None, AnnotationType.VARARG): error_codes.ANN002,
    # ANN001 Missing type annotation for function argument
    AT(True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.ARGS): error_codes.ANN001,
    AT(True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.ARGS): error_codes.ANN001,
    AT(True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.ARGS): error_codes.ANN001,
    AT(True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.POSONLYARGS): error_codes.ANN001,
    AT(True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.POSONLYARGS): error_codes.ANN001,
    AT(
        True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.POSONLYARGS
    ): error_codes.ANN001,
    AT(True, False, None, AnnotationType.ARGS): error_codes.ANN001,
    AT(False, True, None, AnnotationType.ARGS): error_codes.ANN001,
    AT(False, False, None, AnnotationType.ARGS): error_codes.ANN001,
    AT(True, False, None, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(False, True, None, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(False, False, None, AnnotationType.KWONLYARGS): error_codes.ANN001,
    AT(True, False, None, AnnotationType.POSONLYARGS): error_codes.ANN001,
    AT(False, True, None, AnnotationType.POSONLYARGS): error_codes.ANN001,
    AT(False, False, None, AnnotationType.POSONLYARGS): error_codes.ANN001,
}
