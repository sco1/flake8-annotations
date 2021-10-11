# Changelog
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`<major>`.`<minor>`.`<patch>`)

## [v2.7.0]
### Added
* #122 Add support for Flake8 v4.x
### Fixed
* #117 Stop including `CHANGELOG.md` when building wheels.

## [v2.6.2]
### Fixed
* #107, #108 Change incorrect column index yielded for return annotation errors.

## [v2.6.1]
### Changed
* Remove the explicitly pinned minor version ceiling for flake8.

## [v2.6.0]
### Added
* #98 Add `--dispatch-decorators` to support suppression of all errors from functions decorated by decorators such as `functools.singledispatch` and `functools.singledispatchmethod`.
* #99 Add `--overload-decorators` to support generic aliasing of the `typing.overload` decorator.

### Fixed
* #106 Fix incorrect parsing of multiline docstrings with less than two lines of content, causing incorrect line numbers for yielded errors in Python versions prior to 3.8

## [v2.5.0]
### Added
* #103 Add `--allow-untyped-nested` to suppress all errors from dynamically typted nested functions. A function is considered dynamically typed if it does not contain any type hints.

## [v2.4.1]
### Fixed
* #100 Fix incorrect positioning of posonlyargs in the `Function` argument list, causing incorrect classification of the type of missing argument.

## [v2.4.0]
### Fixed
* #92 Fix inconsistent linting behavior between function-level type comments and their equivalent PEP 3107-style function annotations of class methods and classmethods.
* #94 Fix improper handling of the closing definition in a series of `typing.overload` decorated functions.

## [v2.3.0]
### Added
* #87 Add `--mypy-init-return` to allow omission of a return type hint for `__init__` if at least one argument is annotated. See [mypy's documentation](https://mypy.readthedocs.io/en/stable/class_basics.html?#annotating-init-methods) for additional details.

## [v2.2.1]
### Fixed
* #89 Revert change to Python version pinning to prevent unnecessary locking headaches

## [v2.2.0]
### Added
* #87 Add `--allow-untyped-defs` to suppress all errors from dynamically typed functions. A function is considered dynamically typed if it does not contain any type hints.

### Fixed
* #77, #81 Fix incorrect return error locations in the presence of a multiline docstring containing colon(s)
* #81 Fix incorrect return error locations for single-line function definitions
* Fix incorrectly pinned project specifications

## [v2.1.0]
### Added
* #68 Add `--suppress-dummy-args` configuration option to suppress ANN000 level errors for dummy arguments, defined as `"_"`

## [v2.0.1]
### Added
* #71 Add `pep8-naming` to linting toolchain
* Expand pre-commit hooks
  * Add `black`
  * Add `check-merge-conflict`
  * Add `check-toml`
  * Add `check-yaml`
  * Add `end-of-file-fixer`
  * Add `mixed-line-ending`
  * Add `python-check-blanket-noqa`

### Changed
* Add argument names to `Argument` and `Function` `__repr__` methods to make the string more helpful to read

### Fixed
* #70 Fix incorrect column index for missing return annotations when other annotations are present on the same line of source
* #69 Fix misclassification of `None` returning functions when they contained nested functions with non-`None` returns (thanks @isidentical!)
* #67 Fix methods of nested classes being improperly classified as "regular" functions (thanks @isidentical!)

## [v2.0.0]
### Changed
* #64 Change prefix from `TYP` to `ANN` in order to deconflict with `flake8-typing-imports`

## [v1.2.0]
### Added
* Add test case for checking whether flake8 invokes our plugin
* #41 Add `--suppress-none-returning` configuration option to suppress TYP200 level errors for functions that either lack a `return` statement or only explicitly return `None`.
* Add `black` as an explicit developer requirement (codebase already adheres to `black` formatting)

### Changed
* #61 Migrate from Pipenv to Poetry for developer environment setup

## [v1.1.3]
### Fixed
* Add missing classifier test cases for POSONLYARGS
* Re-add the `tree` argument to the checker so flake8 identifies the plugin as needing to run

## [v1.1.2]
### Changed
* Request source from `flake8` as lines of code rather than parsing it from the requested filename ourselves, allowing for proper parsing of `stdin` inputs
* Remove `flake8-string-format` from dev dependencies, as `str.format()` isn't used anywhere

### Fixed
* #52 Fix error when invoking with `stdin` source code instead of a filename

## [v1.1.1]
### Added
* Add [`pipenv-setup`](https://github.com/Madoshakalaka/pipenv-setup) as a dev dependency & CI check to ensure synchronization between `Pipfile` and `setup.py`
* Add [tox](https://github.com/tox-dev/tox) configuration for local testing across Python versions
* Add test for checking a single yield of TYP301 per function
* Add coverage reporting to test suite
* Add testing for positional only arguments

### Changed
* [`typed_ast`](https://github.com/python/typed_ast) is now required only for Python versions `< 3.8`
* Update flake8 minimum version to `3.7.9` for Python 3.8 compatibility
* #50 Completely refactor test suite for maintainability

### Fixed
* Fix mixed type hint tests not being run due to misnamed test class
* Fix `TYP301` classification issue where error is not yielded if the first argument is type annotated and the remaining arguments have type comments

## [v1.1.0]
### Added
* #35: Issue templates
* #36: Support for PEP 484-style type comments
* #36: Add `TYP301` for presence of type comment & type annotation for same entity
* #36: Add `error_code.from_function` class method to generate argument for an entire function
* #18: PyPI release via GitHub Action
* #38: Improve `setup.py` metadata

### Fixed
* #32: Incorrect line number for return values in the presence of multiline docstrings
* #33: Improper handling of nested functions in class methods
* `setup.py` dev dependencies out of sync with Pipfile
* Incorrect order of arguments in `Argument` and `Function` `__repr__` methods

## [v1.0.0] - 2019-09-09
Initial release
