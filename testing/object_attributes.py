from flake8_annotations import error_codes
from flake8_annotations.enums import ClassDecoratorType, FunctionType

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
