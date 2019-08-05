from ast_adventures import __version__


class TypeHintChecker:
    """Top level checker for linting the presence of type hints in function definitions."""

    name = "type-hints"
    version = __version__

    def __init__(self, tree, filename, lines):
        raise NotImplementedError
