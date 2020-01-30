from argparse import Namespace
from functools import lru_cache
from typing import Generator, List

from flake8.options.manager import OptionManager
from flake8_annotations import (
    Argument,
    Function,
    FunctionVisitor,
    PY_GTE_38,
    __version__,
    enums,
    error_codes,
)

# Check if we can use the stdlib ast module instead of typed_ast
# stdlib ast gains native type comment support in Python 3.8
if PY_GTE_38:
    import ast
else:
    from typed_ast import ast3 as ast


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "flake8-annotations"
    version = __version__

    def __init__(self, tree: ast.Module, lines: List[str]):
        # Request `tree` in order to ensure flake8 will run the plugin, even though we don't use it
        # Request `lines` here and join to allow for correct handling of input from stdin
        self.lines = lines
        self.tree = self.get_typed_tree("".join(lines))  # flake8 doesn't strip newlines

    def run(self) -> Generator[error_codes.Error, None, None]:
        """
        This method is called by flake8 to perform the actual check(s) on the source code.

        This should yield tuples with the following information:
          (line number, column number, message, checker type)
        """
        visitor = FunctionVisitor(self.lines)
        visitor.visit(self.tree)

        # Iterate over the arguments with missing type hints, by function, and yield linting errors
        # to flake8
        #
        # Flake8 handles all noqa and error code ignore configurations after the error is yielded
        for function in visitor.function_definitions:
            # Create sentinels to check for mixed hint styles
            if function.has_type_comment:
                has_type_comment = True
            else:
                has_type_comment = False

            has_3107_annotation = False  # 3107 annotations are captured by the return arg

            # Iterate over annotated args to detect mixing of type annotations and type comments
            # Emit this only once per function definition
            for arg in function.get_annotated_arguments():
                if arg.has_type_comment:
                    has_type_comment = True

                if arg.has_3107_annotation:
                    has_3107_annotation = True

                if has_type_comment and has_3107_annotation:
                    # Short-circuit check for mixing of type comments & 3107-style annotations
                    yield error_codes.ANN301.from_function(function).to_flake8()
                    break

            # Yield explicit errors for arguments that are missing annotations
            for arg in function.get_missed_annotations():
                # Skip yielding return errors if the `--suppress-none-returning` flag is True and
                # the function has only `None` returns (which includes the case of no returns)
                if arg.argname == "return" and self.suppress_none_returning:
                    if not arg.has_type_annotation and function.has_only_none_returns:
                        continue

                yield classify_error(function, arg).to_flake8()

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Add custom configuration option(s) to flake8."""
        parser.add_option(
            "--suppress-none-returning",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Suppress ANN200-level errors for functions that contain no return statement or "
                "contain only bare return statements. (Default: False)"
            ),
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        """Parse the custom configuration options given to flake8."""
        cls.suppress_none_returning = options.suppress_none_returning

    @staticmethod
    def get_typed_tree(src: str) -> ast.Module:
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
) -> error_codes.Error:
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
) -> error_codes.Error:
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
