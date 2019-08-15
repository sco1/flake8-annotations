from flake8_annotations import error_codes
from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType

# Build a dictionary of possible function combinations & the resultant error code
# Keys are tuples of the form (function type, is class method?, class decorator type)
return_classifications = {
    # TYP206 Missing return type annotation for classmethod
    (FunctionType.PUBLIC, True, ClassDecoratorType.CLASSMETHOD): error_codes.TYP206,
    (FunctionType.PROTECTED, True, ClassDecoratorType.CLASSMETHOD): error_codes.TYP206,
    (FunctionType.PRIVATE, True, ClassDecoratorType.CLASSMETHOD): error_codes.TYP206,
    (FunctionType.SPECIAL, True, ClassDecoratorType.CLASSMETHOD): error_codes.TYP206,
    # TYP205 Missing return type annotation for staticmethod
    (FunctionType.PUBLIC, True, ClassDecoratorType.STATICMETHOD): error_codes.TYP205,
    (FunctionType.PROTECTED, True, ClassDecoratorType.STATICMETHOD): error_codes.TYP205,
    (FunctionType.PRIVATE, True, ClassDecoratorType.STATICMETHOD): error_codes.TYP205,
    (FunctionType.SPECIAL, True, ClassDecoratorType.STATICMETHOD): error_codes.TYP205,
    # TYP204 Missing return type annotation for special method
    (FunctionType.SPECIAL, True, None): error_codes.TYP204,
    (FunctionType.SPECIAL, False, None): error_codes.TYP204,
    # TYP203 Missing return type annotation for secret function
    (FunctionType.PRIVATE, True, None): error_codes.TYP203,
    (FunctionType.PRIVATE, False, None): error_codes.TYP203,
    # TYP202 Missing return type annotation for protected function
    (FunctionType.PROTECTED, True, None): error_codes.TYP202,
    (FunctionType.PROTECTED, False, None): error_codes.TYP202,
    # TYP201 Missing return type annotation for public function
    (FunctionType.PUBLIC, True, None): error_codes.TYP201,
    (FunctionType.PUBLIC, False, None): error_codes.TYP201,
}

# Build a dictionary of possible argument combinations & the resultant error code
# Keys are tuples of the form (is_class_method, is_first_arg, decorator_type, annotation_type)
argument_classifications = {
    # TYP102 Missing type annotation for cls in classmethod
    (True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.ARGS): error_codes.TYP102,
    (True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.VARARG): error_codes.TYP102,
    (True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWONLYARGS): error_codes.TYP102,
    (True, True, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWARG): error_codes.TYP102,
    # TYP101 Missing type annotation for self in method
    (True, True, None, AnnotationType.ARGS): error_codes.TYP101,
    (True, True, None, AnnotationType.VARARG): error_codes.TYP101,
    (True, True, None, AnnotationType.KWONLYARGS): error_codes.TYP101,
    (True, True, None, AnnotationType.KWARG): error_codes.TYP101,
    # TYP003 Missing type annotation for **kwargs
    (True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWARG): error_codes.TYP003,
    (True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.KWARG): error_codes.TYP003,
    (True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.KWARG): error_codes.TYP003,
    (True, False, None, AnnotationType.KWARG): error_codes.TYP003,
    (False, True, None, AnnotationType.KWARG): error_codes.TYP003,
    (False, False, None, AnnotationType.KWARG): error_codes.TYP003,
    # TYP002 Missing type annotation for *args
    (True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.VARARG): error_codes.TYP002,
    (True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.VARARG): error_codes.TYP002,
    (True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.VARARG): error_codes.TYP002,
    (True, False, None, AnnotationType.VARARG): error_codes.TYP002,
    (False, True, None, AnnotationType.VARARG): error_codes.TYP002,
    (False, False, None, AnnotationType.VARARG): error_codes.TYP002,
    # TYP001 Missing type annotation for function argument
    (True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.ARGS): error_codes.TYP001,
    (True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.ARGS): error_codes.TYP001,
    (True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.ARGS): error_codes.TYP001,
    (True, False, None, AnnotationType.ARGS): error_codes.TYP001,
    (False, True, None, AnnotationType.ARGS): error_codes.TYP001,
    (False, False, None, AnnotationType.ARGS): error_codes.TYP001,
    (True, False, ClassDecoratorType.CLASSMETHOD, AnnotationType.KWONLYARGS): error_codes.TYP001,
    (True, True, ClassDecoratorType.STATICMETHOD, AnnotationType.KWONLYARGS): error_codes.TYP001,
    (True, False, ClassDecoratorType.STATICMETHOD, AnnotationType.KWONLYARGS): error_codes.TYP001,
    (True, False, None, AnnotationType.KWONLYARGS): error_codes.TYP001,
    (False, True, None, AnnotationType.KWONLYARGS): error_codes.TYP001,
    (False, False, None, AnnotationType.KWONLYARGS): error_codes.TYP001,
}
