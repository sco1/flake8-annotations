from __future__ import annotations

import typing as t
from functools import lru_cache

from flake8_annotations import PY_GTE_38, __version__, enums, error_codes
from flake8_annotations.ast_walker import FunctionVisitor, ast

if t.TYPE_CHECKING:
    from argparse import Namespace

    from flake8.options.manager import OptionManager

    from flake8_annotations.ast_walker import Argument, Function

FORMATTED_ERROR = t.Tuple[int, int, str, t.Type[t.Any]]

_DEFAULT_DISPATCH_DECORATORS = [
    "singledispatch",
    "singledispatchmethod",
]

_DEFAULT_OVERLOAD_DECORATORS = [
    "overload",
]

_DISABLED_BY_DEFAULT = ("ANN401",)  # Disable opinionated warnings by default


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "flake8-annotations"
    version = __version__

    def __init__(self, tree: t.Optional[ast.Module], lines: t.List[str]):
        # Request `tree` in order to ensure flake8 will run the plugin, even though we don't use it
        # Request `lines` here and join to allow for correct handling of input from stdin
        self.lines = lines
        self.tree = self.get_typed_tree("".join(lines))  # flake8 doesn't strip newlines

        # Set by flake8's config parser
        self.suppress_none_returning: bool
        self.suppress_dummy_args: bool
        self.allow_untyped_defs: bool
        self.allow_untyped_nested: bool
        self.mypy_init_return: bool
        self.allow_star_arg_any: bool
        self.dispatch_decorators: t.Set[str]
        self.overload_decorators: t.Set[str]

    def run(self) -> t.Generator[FORMATTED_ERROR, None, None]:
        """
        This method is called by flake8 to perform the actual check(s) on the source code.

        This should yield tuples with the following information:
          (line number, column number, message, checker type)
        """
        visitor = FunctionVisitor(self.lines)
        visitor.visit(self.tree)

        # Keep track of the last encountered function decorated by `typing.overload`, if any.
        # Per the `typing` module documentation, a series of overload-decorated definitions must be
        # followed by exactly one non-overload-decorated definition of the same function.
        last_overload_decorated_function_name: t.Optional[str] = None

        # Iterate over the arguments with missing type hints, by function, and yield linting errors
        # to flake8
        #
        # Flake8 handles all noqa and error code ignore configurations after the error is yielded
        for function in visitor.function_definitions:
            if function.is_dynamically_typed():
                if self.allow_untyped_defs:
                    # Skip yielding errors from dynamically typed functions
                    continue
                elif function.is_nested and self.allow_untyped_nested:
                    # Skip yielding errors from dynamically typed nested functions
                    continue

            # Skip yielding errors for configured dispatch functions, such as (by default)
            # `functools.singledispatch` and `functools.singledispatchmethod`
            if function.has_decorator(self.dispatch_decorators):
                continue

            # Create sentinels to check for mixed hint styles
            if function.has_type_comment:
                has_type_comment = True
            else:
                has_type_comment = False

            has_3107_annotation = False  # 3107 annotations are captured by the return arg

            # Iterate over annotated args to detect mixing of type annotations and type comments
            # Emit this only once per function definition
            annotated_args = function.get_annotated_arguments()
            for arg in annotated_args:
                if arg.has_type_comment:
                    has_type_comment = True

                if arg.has_3107_annotation:
                    has_3107_annotation = True

                if has_type_comment and has_3107_annotation:
                    # Short-circuit check for mixing of type comments & 3107-style annotations
                    yield error_codes.ANN301.from_function(function).to_flake8()
                    break

            # Iterate over the annotated args to look for `typing.Any` annotations
            # We could combine this with the above loop but I'd rather not add even more sentinels
            # unless we'd notice a significant enough performance impact
            for arg in annotated_args:
                if arg.is_dynamically_typed:
                    if self.allow_star_arg_any and arg.annotation_type in {
                        enums.AnnotationType.VARARG,
                        enums.AnnotationType.KWARG,
                    }:
                        continue

                    yield error_codes.ANN401.from_argument(arg).to_flake8()

            # Before we iterate over the function's missing annotations, check to see if it's the
            # closing function def in a series of `typing.overload` decorated functions.
            if last_overload_decorated_function_name == function.name:
                continue

            # If it's not, and it is overload decorated, store it for the next iteration
            if function.has_decorator(self.overload_decorators):
                last_overload_decorated_function_name = function.name

            # Yield explicit errors for arguments that are missing annotations
            for arg in function.get_missed_annotations():
                if arg.argname == "return":
                    # return annotations have multiple possible short-circuit paths
                    if self.suppress_none_returning:
                        # Skip yielding return errors if the function has only `None` returns
                        # This includes the case of no returns.
                        if function.has_only_none_returns:
                            continue
                    if self.mypy_init_return:
                        # Skip yielding return errors for `__init__` if at least one argument is
                        # annotated
                        if function.is_class_method and function.name == "__init__":
                            # If we've gotten here, then our annotated args won't contain "return"
                            # since we're in a logic check for missing "return". So if our annotated
                            # are non-empty, then __init__ has at least one annotated argument
                            if annotated_args:
                                continue

                # If the `--suppress-dummy-args` flag is `True`, skip yielding errors for any
                # arguments named `_`
                if arg.argname == "_" and self.suppress_dummy_args:
                    continue

                yield classify_error(function, arg).to_flake8()

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:  # pragma: no cover
        """Add custom configuration option(s) to flake8."""
        parser.extend_default_ignore(_DISABLED_BY_DEFAULT)

        parser.add_option(
            "--suppress-none-returning",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Suppress ANN200-level errors for functions that contain no return statement or "
                "contain only bare return statements. (Default: %(default)s)"
            ),
        )

        parser.add_option(
            "--suppress-dummy-args",
            default=False,
            action="store_true",
            parse_from_config=True,
            help="Suppress ANN000-level errors for dummy arguments, defined as '_'. (Default: %(default)s)",  # noqa: E501
        )

        parser.add_option(
            "--allow-untyped-defs",
            default=False,
            action="store_true",
            parse_from_config=True,
            help="Suppress all errors for dynamically typed functions. (Default: %(default)s)",
        )

        parser.add_option(
            "--allow-untyped-nested",
            default=False,
            action="store_true",
            parse_from_config=True,
            help="Suppress all errors for dynamically typed nested functions. (Default: %(default)s)",  # noqa: E501
        )

        parser.add_option(
            "--mypy-init-return",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Allow omission of a return type hint for __init__ if at least one argument is "
                "annotated. (Default: %(default)s)"
            ),
        )

        parser.add_option(
            "--dispatch-decorators",
            default=_DEFAULT_DISPATCH_DECORATORS,
            action="store",
            type=str,
            parse_from_config=True,
            comma_separated_list=True,
            help=(
                "Comma-separated list of decorators flake8-annotations should consider as dispatch "
                "decorators. (Default: %(default)s)"
            ),
        )

        parser.add_option(
            "--overload-decorators",
            default=_DEFAULT_OVERLOAD_DECORATORS,
            action="store",
            type=str,
            parse_from_config=True,
            comma_separated_list=True,
            help=(
                "Comma-separated list of decorators flake8-annotations should consider as "
                "typing.overload decorators. (Default: %(default)s)"
            ),
        )

        parser.add_option(
            "--allow-star-arg-any",
            default=False,
            action="store_true",
            parse_from_config=True,
            help="Suppress ANN401 for dynamically typed *args and **kwargs. (Default: %(default)s)",
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> None:  # pragma: no cover
        """Parse the custom configuration options given to flake8."""
        cls.suppress_none_returning = options.suppress_none_returning
        cls.suppress_dummy_args = options.suppress_dummy_args
        cls.allow_untyped_defs = options.allow_untyped_defs
        cls.allow_untyped_nested = options.allow_untyped_nested
        cls.mypy_init_return = options.mypy_init_return
        cls.allow_star_arg_any = options.allow_star_arg_any

        # Store decorator lists as sets for easier lookup
        cls.dispatch_decorators = set(options.dispatch_decorators)
        cls.overload_decorators = set(options.overload_decorators)

    @staticmethod
    def get_typed_tree(src: str) -> ast.Module:  # pragma: no cover
        """Parse the provided source into a typed AST."""
        if PY_GTE_38:
            # Built-in ast requires a flag to parse type comments
            tree = ast.parse(src, type_comments=True)
        else:
            # typed-ast will implicitly parse type comments
            tree = ast.parse(src)

        return tree


def classify_error(function: Function, arg: Argument) -> error_codes.Error:
    """
    Classify the missing type annotation based on the Function & Argument metadata.

    For the currently defined rules & program flow, the assumption can be made that an argument
    passed to this method will match a linting error, and will only match a single linting error

    This function provides an initial classificaton, then passes relevant attributes to cached
    helper function(s).
    """
    # Check for return type
    # All return "arguments" have an explicitly defined name "return"
    if arg.argname == "return":
        error_code = _return_error_classifier(
            function.is_class_method, function.class_decorator_type, function.function_type
        )
    else:
        # Otherwise, classify function argument error
        is_first_arg = arg == function.args[0]
        error_code = _argument_error_classifier(
            function.is_class_method,
            is_first_arg,
            function.class_decorator_type,
            arg.annotation_type,
        )

    return error_code.from_argument(arg)


@lru_cache()
def _return_error_classifier(
    is_class_method: bool,
    class_decorator_type: enums.ClassDecoratorType,
    function_type: enums.FunctionType,
) -> t.Type[error_codes.Error]:
    """Classify return type annotation error."""
    # Decorated class methods (@classmethod, @staticmethod) have a higher priority than the rest
    if is_class_method:
        if class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
            return error_codes.ANN206
        elif class_decorator_type == enums.ClassDecoratorType.STATICMETHOD:
            return error_codes.ANN205

    if function_type == enums.FunctionType.SPECIAL:
        return error_codes.ANN204
    elif function_type == enums.FunctionType.PRIVATE:
        return error_codes.ANN203
    elif function_type == enums.FunctionType.PROTECTED:
        return error_codes.ANN202
    else:
        return error_codes.ANN201


@lru_cache()
def _argument_error_classifier(
    is_class_method: bool,
    is_first_arg: bool,
    class_decorator_type: enums.ClassDecoratorType,
    annotation_type: enums.AnnotationType,
) -> t.Type[error_codes.Error]:
    """Classify argument type annotation error."""
    # Check for regular class methods and @classmethod, @staticmethod is deferred to final check
    if is_class_method:
        # The first function argument here would be an instance of self or class
        if is_first_arg:
            if class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
                return error_codes.ANN102
            elif class_decorator_type != enums.ClassDecoratorType.STATICMETHOD:
                # Regular class method
                return error_codes.ANN101

    # Check for remaining codes
    if annotation_type == enums.AnnotationType.KWARG:
        return error_codes.ANN003
    elif annotation_type == enums.AnnotationType.VARARG:
        return error_codes.ANN002
    else:
        # Combine POSONLYARG, ARG, and KWONLYARGS
        return error_codes.ANN001
