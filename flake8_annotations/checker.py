from functools import lru_cache
from typing import List

import pycodestyle
from flake8_annotations import Argument, Function, FunctionVisitor, __version__, enums, error_codes


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "function-type-annotations"
    version = __version__

    def __init__(self, tree, lines: List[str]):
        self.tree = tree
        self.lines = lines

    def run(self):
        """
        This method is called by flake8 to perform the actual check(s) on the source code.

        This should yield tuples with the following information:
          (line number, column number, message, checker type)
        """
        visitor = FunctionVisitor()
        visitor.visit(self.tree)

        # Iterate over the arguments with missing type hints, by function, and determine whether an
        # error should be yielded to flake8
        for function in visitor.function_definitions:
            for arg in function.get_missed_annotations():
                # Check for noqa first
                if pycodestyle.noqa(self.lines[arg.lineno - 1]):  # lineno is 1-indexed
                    continue

                yield classify_error(function, arg).to_flake8()


def classify_error(function: Function, arg: Argument) -> error_codes.Error:
    """
    Classify the missing type annotation based on the Function & Argument metadata.

    For the currently defined rules & program flow, the assumption can be made that an argument
    passed to this method will match a linting error, and will only match a single linting error
    """
    # Check for return type
    # All return "arguments" have an explicitly defined name "return"
    if arg.argname == "return":
        # Decorated class methods (@classmethod, @staticmethod) have a higher priority than the rest
        if function.is_class_method:
            if function.class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
                return error_codes.TYP206.from_argument(arg)
            elif function.class_decorator_type == enums.ClassDecoratorType.STATICMETHOD:
                return error_codes.TYP205.from_argument(arg)

        if function.function_type == enums.FunctionType.MAGIC:
            return error_codes.TYP204.from_argument(arg)
        elif function.function_type == enums.FunctionType.PRIVATE:
            return error_codes.TYP203.from_argument(arg)
        elif function.function_type == enums.FunctionType.PROTECTED:
            return error_codes.TYP202.from_argument(arg)
        else:
            return error_codes.TYP201.from_argument(arg)

    # Check for regular class methods and @classmethod, @staticmethod is deferred to final check
    if function.is_class_method:
        # The first function argument here would be an instance of self or class
        if arg == function.args[0]:
            if function.class_decorator_type == enums.ClassDecoratorType.CLASSMETHOD:
                return error_codes.TYP102.from_argument(arg)
            elif function.class_decorator_type != enums.ClassDecoratorType.STATICMETHOD:
                # Regular class method
                return error_codes.TYP101.from_argument(arg)

    # Check for remaining codes
    if arg.annotation_type == enums.AnnotationType.KWARG:
        return error_codes.TYP003.from_argument(arg)
    elif arg.annotation_type == enums.AnnotationType.VARARG:
        return error_codes.TYP002.from_argument(arg)
    else:
        # Combine ARG and KWONLYARGS
        return error_codes.TYP001.from_argument(arg)
