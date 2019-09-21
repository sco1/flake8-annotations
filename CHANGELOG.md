# Changelog
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`<major>`.`<minor>`.`<patch>`)

## [Unreleased]
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