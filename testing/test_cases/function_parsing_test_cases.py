from functools import partial
from textwrap import dedent
from typing import NamedTuple, Tuple

from flake8_annotations import Function
from flake8_annotations.enums import ClassDecoratorType, FunctionType


class FunctionTestCase(NamedTuple):
    """Helper container for Function parsing test cases."""

    src: str
    func: Tuple[Function]


# Note: For testing purposes, lineno and col_offset are ignored so these are set to dummy values
# using partial objects
nonclass_func = partial(
    Function, lineno=0, col_offset=0, is_class_method=False, class_decorator_type=None
)
class_func = partial(Function, lineno=0, col_offset=0, is_class_method=True)

function_test_cases = {
    "public_fun": FunctionTestCase(
        src=dedent(
            """\
            def foo():
                pass
            """
        ),
        func=(nonclass_func(name="foo", function_type=FunctionType.PUBLIC),),
    ),
    "public_fun_return_annotated": FunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                pass
            """
        ),
        func=(
            nonclass_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                is_return_annotated=True,
            ),
        ),
    ),
    "protected_fun": FunctionTestCase(
        src=dedent(
            """\
            def _foo():
                pass
            """
        ),
        func=(nonclass_func(name="_foo", function_type=FunctionType.PROTECTED),),
    ),
    "private_fun": FunctionTestCase(
        src=dedent(
            """\
            def __foo():
                pass
            """
        ),
        func=(nonclass_func(name="__foo", function_type=FunctionType.PRIVATE),),
    ),
    "special_fun": FunctionTestCase(
        src=dedent(
            """\
            def __foo__():
                pass
            """
        ),
        func=(nonclass_func(name="__foo__", function_type=FunctionType.SPECIAL),),
    ),
    "async_public_fun": FunctionTestCase(
        src=dedent(
            """\
            async def foo():
                pass
            """
        ),
        func=(nonclass_func(name="foo", function_type=FunctionType.PUBLIC),),
    ),
    "async_public_fun_return_annotated": FunctionTestCase(
        src=dedent(
            """\
            async def foo() -> None:
                pass
            """
        ),
        func=(
            nonclass_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                is_return_annotated=True,
            ),
        ),
    ),
    "async_protected_fun": FunctionTestCase(
        src=dedent(
            """\
            async def _foo():
                pass
            """
        ),
        func=(nonclass_func(name="_foo", function_type=FunctionType.PROTECTED),),
    ),
    "async_private_fun": FunctionTestCase(
        src=dedent(
            """\
            async def __foo():
                pass
            """
        ),
        func=(nonclass_func(name="__foo", function_type=FunctionType.PRIVATE),),
    ),
    "async_special_fun__": FunctionTestCase(
        src=dedent(
            """\
            async def __foo__():
                pass
            """
        ),
        func=(nonclass_func(name="__foo__", function_type=FunctionType.SPECIAL),),
    ),
    "double_nested_public_no_return_annotation": FunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar():
                    def baz():
                        pass
            """
        ),
        func=(
            nonclass_func(name="foo", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC),
        ),
    ),
    "double_nested_public_return_annotation": FunctionTestCase(
        src=dedent(
            """\
            def foo() -> None:
                def bar() -> None:
                    def baz() -> None:
                        pass
            """
        ),
        func=(
            nonclass_func(name="foo", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC, is_return_annotated=True),
        ),
    ),
    "double_nested_public_async_no_return_annotation": FunctionTestCase(
        src=dedent(
            """\
            async def foo() -> None:
                async def bar():
                    async def baz():
                        pass
            """
        ),
        func=(
            nonclass_func(name="foo", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC),
        ),
    ),
    "double_nested_public_async_return_annotation": FunctionTestCase(
        src=dedent(
            """\
            async def foo() -> None:
                async def bar() -> None:
                    async def baz() -> None:
                        pass
            """
        ),
        func=(
            nonclass_func(name="foo", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC, is_return_annotated=True),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC, is_return_annotated=True),
        ),
    ),
    "decorated_noncallable_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                def foo(self):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
            ),
        ),
    ),
    "decorated_callable_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                def foo(self):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
            ),
        ),
    ),
    "decorated_noncallable_async_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                async def foo(self):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
            ),
        ),
    ),
    "decorated_callable_async_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                async def foo(self):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
            ),
        ),
    ),
    "decorated_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @classmethod
                def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @staticmethod
                def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "decorated_async_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @classmethod
                async def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_async_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @staticmethod
                async def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "decorated_noncallable_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                @classmethod
                def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_callable_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                @classmethod
                def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_noncallable_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                @staticmethod
                def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "decorated_callable_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                @staticmethod
                def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "decorated_noncallable_async_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                @classmethod
                async def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_callable_async_classmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                @classmethod
                async def foo(cls):
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.CLASSMETHOD,
            ),
        ),
    ),
    "decorated_noncallable_async_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator
                @staticmethod
                async def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "decorated_callable_async_staticmethod": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                @some_decorator()
                @staticmethod
                async def foo():
                    pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=ClassDecoratorType.STATICMETHOD,
            ),
        ),
    ),
    "double_nested_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                def foo(self) -> None:
                    def bar():
                        def baz():
                            pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
                is_return_annotated=True,
            ),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC),
        ),
    ),
    "double_nested_async_method": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                async def foo(self) -> None:
                    async def bar():
                        async def baz():
                            pass
            """
        ),
        func=(
            class_func(
                name="foo",
                function_type=FunctionType.PUBLIC,
                class_decorator_type=None,
                is_return_annotated=True,
            ),
            nonclass_func(name="bar", function_type=FunctionType.PUBLIC),
            nonclass_func(name="baz", function_type=FunctionType.PUBLIC),
        ),
    ),
    "nested_classes": FunctionTestCase(
        src=dedent(
            """\
            class Foo:
                class Bar:
                    def bar_method(self):
                        pass

                def foo_method(self):
                    pass
            """
        ),
        func=(
            class_func(name="bar_method", function_type=FunctionType.PUBLIC),
            class_func(name="foo_method", function_type=FunctionType.PUBLIC),
        ),
    ),
    "overload_decorated_non_alias": FunctionTestCase(
        src=dedent(
            """\
            @overload
            def foo():
                pass
            """
        ),
        func=(
            nonclass_func(
                name="foo", function_type=FunctionType.PUBLIC, is_overload_decorated=True,
            ),
        ),
    ),
    "overload_decorated_attribute": FunctionTestCase(
        src=dedent(
            """\
            @typing.overload
            def foo():
                pass
            """
        ),
        func=(
            nonclass_func(
                name="foo", function_type=FunctionType.PUBLIC, is_overload_decorated=True,
            ),
        ),
    ),
}
