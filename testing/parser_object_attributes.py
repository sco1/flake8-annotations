from flake8_annotations import Argument, Function
from flake8_annotations.enums import AnnotationType, FunctionType, ClassDecoratorType

# Build a dictionary of Argument objects corresponding to what we should be getting out of the
# argument parsing test
# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
parsed_arguments = {
    "all_args_untyped": [
        Argument(argname="arg", lineno=0, col_offset=0, annotation_type=AnnotationType.ARGS),
        Argument(argname="vararg", lineno=0, col_offset=0, annotation_type=AnnotationType.VARARG),
        Argument(
            argname="kwonlyarg", lineno=0, col_offset=0, annotation_type=AnnotationType.KWONLYARGS
        ),  # noqa
        Argument(argname="kwarg", lineno=0, col_offset=0, annotation_type=AnnotationType.KWARG),
        Argument(argname="return", lineno=0, col_offset=0, annotation_type=AnnotationType.RETURN),
    ],
    "all_args_typed": [
        Argument(
            argname="arg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.ARGS,
            has_type_annotation=True,
        ),
        Argument(
            argname="vararg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.VARARG,
            has_type_annotation=True,
        ),
        Argument(
            argname="kwonlyarg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.KWONLYARGS,
            has_type_annotation=True,
        ),
        Argument(
            argname="kwarg",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.KWARG,
            has_type_annotation=True,
        ),
        Argument(
            argname="return",
            lineno=0,
            col_offset=0,
            annotation_type=AnnotationType.RETURN,
            has_type_annotation=True,
        ),
    ],
}


parsed_functions = {
    "public_fun": Function(
        name="public_fun",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=False,
        class_decorator_type=None,
    ),
    "public_fun_return_annotated": Function(
        name="public_fun_return_annotated",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=False,
        class_decorator_type=None,
        is_return_annotated=True,
    ),
    "_protected_fun": Function(
        name="_protected_fun",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PROTECTED,
        is_class_method=False,
        class_decorator_type=None,
    ),
    "__private_fun": Function(
        name="__private_fun",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PRIVATE,
        is_class_method=False,
        class_decorator_type=None,
    ),
    "__special_fun__": Function(
        name="__special_fun__",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.SPECIAL,
        is_class_method=False,
        class_decorator_type=None,
    ),
    "decorated_noncallable_method": Function(
        name="decorated_noncallable_method",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=None,
    ),
    "decorated_callable_method": Function(
        name="decorated_callable_method",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=None,
    ),
    "decorated_classmethod": Function(
        name="decorated_classmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_staticmethod": Function(
        name="decorated_staticmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_noncallable_classmethod": Function(
        name="decorated_noncallable_classmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_callable_classmethod": Function(
        name="decorated_callable_classmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_noncallable_staticmethod": Function(
        name="decorated_noncallable_staticmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_callable_staticmethod": Function(
        name="decorated_callable_staticmethod",
        lineno=0,
        col_offset=0,
        function_type=FunctionType.PUBLIC,
        is_class_method=True,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
}
