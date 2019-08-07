import ast
from functools import lru_cache
from typing import Generator, List

from flake8_annotations import Argument, Function, FunctionVisitor, __version__, enums, error_codes


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "function-type-annotations"
    version = __version__

    def __init__(self, tree: ast.Module, lines: List[str]):
        self.tree = tree
        self.lines = lines

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
            for arg in function.get_missed_annotations():
                yield classify_error(function, arg).to_flake8()


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
    # Decorated class methods (@classmethod, @staticmethod, @property) have a higher priority than
    # the rest
    if is_class_method:
        if class_decorator_type == enums.ClassDecoratorType.PROPERTY:
            # Property decorators (property, .getter, .setter, .deleter)
            return error_codes.TYP207
        elif class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
            return error_codes.TYP206
        elif class_decorator_type == enums.ClassDecoratorType.STATICMETHOD:
            return error_codes.TYP205

    if function_type == enums.FunctionType.MAGIC:
        return error_codes.TYP204
    elif function_type == enums.FunctionType.PRIVATE:
        return error_codes.TYP203
    elif function_type == enums.FunctionType.PROTECTED:
        return error_codes.TYP202
    else:
        # "Regular" function declaration
        return error_codes.TYP201


@lru_cache()
def _argument_error_classifier(
    is_class_method: bool,
    is_first_arg: bool,
    class_decorator_type: enums.ClassDecoratorType,
    annotation_type: enums.AnnotationType,
) -> error_codes.Error:
    """Classify argument type annotation error."""
    # Check for regular class methods, @property (includes getter, setter, deleter), & @classmethod
    if is_class_method:
        # The first function argument here would be an instance of self or class
        if is_first_arg:
            if class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
                return error_codes.TYP103
            elif class_decorator_type == enums.ClassDecoratorType.PROPERTY:
                return error_codes.TYP102
            elif class_decorator_type != enums.ClassDecoratorType.STATICMETHOD:
                # Regular class method
                return error_codes.TYP101

    # Check for remaining codes
    if annotation_type == enums.AnnotationType.KWARG:
        return error_codes.TYP003
    elif annotation_type == enums.AnnotationType.VARARG:
        return error_codes.TYP002
    else:
        # Combine ARG and KWONLYARGS
        return error_codes.TYP001
