from functools import partial

from flake8_annotations import Argument, Function
from flake8_annotations.enums import AnnotationType, ClassDecoratorType, FunctionType

# Build a dictionary of Argument objects corresponding to what we should be getting out of the
# argument parsing test
# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
# using partial objects
untyped_arg = partial(Argument, lineno=0, col_offset=0, has_type_annotation=False)
typed_arg = partial(
    Argument, lineno=0, col_offset=0, has_type_annotation=True, has_3107_annotation=True
)
parsed_arguments = {
    "all_args_untyped": [
        untyped_arg(argname="arg", annotation_type=AnnotationType.ARGS),
        untyped_arg(argname="vararg", annotation_type=AnnotationType.VARARG),
        untyped_arg(argname="kwonlyarg", annotation_type=AnnotationType.KWONLYARGS),
        untyped_arg(argname="kwarg", annotation_type=AnnotationType.KWARG),
        untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
    "all_args_typed": [
        typed_arg(argname="arg", annotation_type=AnnotationType.ARGS),
        typed_arg(argname="vararg", annotation_type=AnnotationType.VARARG),
        typed_arg(argname="kwonlyarg", annotation_type=AnnotationType.KWONLYARGS),
        typed_arg(argname="kwarg", annotation_type=AnnotationType.KWARG),
        typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
    ],
}

# Build a dictionary of Function objects corresponding to what we should be getting out of the
# function parsing test
# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
# using partial objects
nonclass_func = partial(
    Function, lineno=0, col_offset=0, is_class_method=False, class_decorator_type=None
)
class_func = partial(Function, lineno=0, col_offset=0, is_class_method=True)
parsed_functions = {
    "public_fun": nonclass_func(name="public_fun", function_type=FunctionType.PUBLIC),
    "public_fun_return_annotated": nonclass_func(
        name="public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "_protected_fun": nonclass_func(name="_protected_fun", function_type=FunctionType.PROTECTED),
    "__private_fun": nonclass_func(name="__private_fun", function_type=FunctionType.PRIVATE),
    "__special_fun__": nonclass_func(name="__special_fun__", function_type=FunctionType.SPECIAL),
    "async_public_fun": nonclass_func(name="async_public_fun", function_type=FunctionType.PUBLIC),
    "nested_public_fun": nonclass_func(name="nested_public_fun", function_type=FunctionType.PUBLIC),
    "double_nested_public_fun": nonclass_func(
        name="double_nested_public_fun", function_type=FunctionType.PUBLIC
    ),
    "nested_public_fun_return_annotated": nonclass_func(
        name="nested_public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "double_nested_public_fun_return_annotated": nonclass_func(
        name="double_nested_public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "async_public_fun_return_annotated": nonclass_func(
        name="async_public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "_async_protected_fun": nonclass_func(
        name="_async_protected_fun", function_type=FunctionType.PROTECTED
    ),
    "__async_private_fun": nonclass_func(
        name="__async_private_fun", function_type=FunctionType.PRIVATE
    ),
    "__async_special_fun__": nonclass_func(
        name="__async_special_fun__", function_type=FunctionType.SPECIAL
    ),
    "nested_async_public_fun": nonclass_func(
        name="nested_async_public_fun", function_type=FunctionType.PUBLIC
    ),
    "double_nested_async_public_fun": nonclass_func(
        name="double_nested_async_public_fun", function_type=FunctionType.PUBLIC
    ),
    "nested_async_public_fun_return_annotated": nonclass_func(
        name="nested_async_public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "double_nested_async_public_fun_return_annotated": nonclass_func(
        name="double_nested_async_public_fun_return_annotated",
        function_type=FunctionType.PUBLIC,
        is_return_annotated=True,
    ),
    "decorated_noncallable_method": class_func(
        name="decorated_noncallable_method",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=None,
    ),
    "decorated_callable_method": class_func(
        name="decorated_callable_method",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=None,
    ),
    "decorated_noncallable_async_method": class_func(
        name="decorated_noncallable_async_method",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=None,
    ),
    "decorated_callable_async_method": class_func(
        name="decorated_callable_async_method",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=None,
    ),
    "decorated_classmethod": class_func(
        name="decorated_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_staticmethod": class_func(
        name="decorated_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_async_classmethod": class_func(
        name="decorated_async_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_async_staticmethod": class_func(
        name="decorated_async_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_noncallable_classmethod": class_func(
        name="decorated_noncallable_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_callable_classmethod": class_func(
        name="decorated_callable_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_noncallable_staticmethod": class_func(
        name="decorated_noncallable_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_callable_staticmethod": class_func(
        name="decorated_callable_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_noncallable_async_classmethod": class_func(
        name="decorated_noncallable_async_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_callable_async_classmethod": class_func(
        name="decorated_callable_async_classmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.CLASSMETHOD,
    ),
    "decorated_noncallable_async_staticmethod": class_func(
        name="decorated_noncallable_async_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "decorated_callable_async_staticmethod": class_func(
        name="decorated_callable_async_staticmethod",
        function_type=FunctionType.PUBLIC,
        class_decorator_type=ClassDecoratorType.STATICMETHOD,
    ),
    "nested_method": nonclass_func(name="nested_method", function_type=FunctionType.PUBLIC),
    "double_nested_method": nonclass_func(
        name="double_nested_method", function_type=FunctionType.PUBLIC
    ),
    "nested_async_method": nonclass_func(
        name="nested_async_method", function_type=FunctionType.PUBLIC
    ),
    "double_nested_async_method": nonclass_func(
        name="double_nested_async_method", function_type=FunctionType.PUBLIC
    ),
}
