from typing import List

import pycodestyle

from ast_adventures import Argument, Function, FunctionVisitor, __version__, error_codes


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "type-hints"
    version = __version__

    def __init__(self, tree, lines: List[str]):
        self.tree = tree
        self.lines = lines

    def run(self):
        """This method is called by flake8 to perform the actual check(s) on the source code."""
        visitor = FunctionVisitor()
        visitor.visit(self.tree)

        # Iterate over the arguments with missing type hints, by function, and determine whether an
        # error should be yielded to flake8
        for function in visitor.function_definitions:
            for arg in function.get_missed_annotations():
                # Check for noqa first
                if pycodestyle.noqa(self.lines[arg.lineno - 1]):  # lineno is 1-indexed
                    continue

                error = self.classify_error(function, arg)
                if self.should_warn(error):
                    yield error.to_flake8()

    def should_warn(self, error: error_codes.Error) -> bool:
        """Determine whether a linting error should be yielded to flake8."""
        raise NotImplementedError

    @staticmethod
    def classify_error(function: Function, arg: Argument) -> error_codes.Error:
        """
        Classify the missing type annotation based on the Function & Argument metadata.

        For the currently defined rules, the assumption can be made that an argument can only match
        a single linting error
        """
        # Check for return type
        # All return "arguments" have an explicitly defined name "return"
        if arg.name == "return":
            raise NotImplementedError

        # Check for @classmethod and @staticmethod
        # The first argument here would be an instance of self or class, which have explicit codes
        if function.is_class_method:
            raise NotImplementedError

        # Check for remaining codes
        raise NotImplementedError
