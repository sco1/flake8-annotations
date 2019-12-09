# flake8-annotations
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations)
![PyPI](https://img.shields.io/pypi/v/flake8-annotations)
[![Build Status](https://dev.azure.com/python-discord/Python%20Discord/_apis/build/status/python-discord.flake8-annotations?branchName=master)](https://dev.azure.com/python-discord/Python%20Discord/_build/latest?definitionId=16&branchName=master)
[![Discord](https://img.shields.io/discord/267624335836053506?color=%237289DA&label=Python%20Discord&logo=discord&logoColor=white)](https://discord.gg/2B963hn)


`flake8-annotations` is a plugin for [Flake8](http://flake8.pycqa.org/en/latest/) that detects the absence of [PEP 3107-style](https://www.python.org/dev/peps/pep-3107/) function annotations and [PEP 484-style](https://www.python.org/dev/peps/pep-0484/#type-comments) type comments  (see: [Caveats](#Caveats-for-PEP-484-style-Type-Comments)).

What this won't do: Check variable annotations (see: [PEP 526](https://www.python.org/dev/peps/pep-0526/)), respect stub files, or replace [mypy's](http://mypy-lang.org/) static type checking.

## Installation

Install from PyPi with your favorite `pip` invocation:

```bash
$ pip install flake8-annotations
```

It will then be run automatically as part of Flake8.

You can verify it's being picked up by invoking the following in your shell:

```bash
$ flake8 --version
3.7.8 (flake8-annotations: 1.1.2, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.7.4 on Darwin
```

## Table of Warnings
### Function Annotations
| ID       | Description                                   |
|----------|-----------------------------------------------|
| `TYP001` | Missing type annotation for function argument |
| `TYP002` | Missing type annotation for `*args`           |
| `TYP003` | Missing type annotation for `**kwargs`        |

### Method Annotations
| ID       | Description                                        |
|----------|----------------------------------------------------|
| `TYP101` | Missing type annotation for `self` in method       |
| `TYP102` | Missing type annotation for `cls` in classmethod   |

### Return Annotations
| ID       | Description                                           |
|----------|-------------------------------------------------------|
| `TYP201` | Missing return type annotation for public function    |
| `TYP202` | Missing return type annotation for protected function |
| `TYP203` | Missing return type annotation for secret function    |
| `TYP204` | Missing return type annotation for special method     |
| `TYP205` | Missing return type annotation for staticmethod       |
| `TYP206` | Missing return type annotation for classmethod        |

### Type Comments
| ID       | Description                                               |
|----------|-----------------------------------------------------------|
| `TYP301` | PEP 484 disallows both type annotations and type comments |

## Caveats for PEP 484-style Type Comments
### Function type comments
Function type comments are assumed to contain both argument and return type hints

Yes:
```py
# type: (int, int) -> bool
```

No:
```py
# type: (int, int)
```

Python cannot parse the latter and will raise `SyntaxError: unexpected EOF while parsing`

### Mixing argument type comments and function type comments
Support is provided for mixing argument and function type comments, provided that the function type comment use an Ellipsis for the arguments.

```py
def foo(
    arg1,  # type: bool
    arg2,  # type: bool
):  # type: (...) -> bool
    pass
```

Ellipes are ignored by `flake8-annotations` parser.

**Note:** If present, function type comments will override any argument type comments.

### Partial type comments
Partially type hinted functions are supported

For example:

```py
def foo(arg1, arg2):
    # type: (bool) -> bool
    pass
```
Will show `arg2` as missing a type hint.

```py
def foo(arg1, arg2):
    # type: (..., bool) -> bool
    pass
```
Will show `arg1` as missing a type hint.

## Contributing
Please take some time to read through our [contributing guidelines](CONTRIBUTING.md) before helping us with this project.

### Development Environment
This project uses [Pipenv](https://docs.pipenv.org/en/latest/) to manage dependencies. With your fork cloned to your local machine, you can create a developer environment using:

```bash
$ pipenv sync --dev
```

Note: flake8-annotations is included in the Pipfile as an editable dependency so it will be included when flake8 is invoked in your developer environment.

A [pre-commit](https://pre-commit.com) installation script and configuration is also provided to create a pre-commit hook so linting errors aren't committed:

```bash
$ pipenv run precommit
```

### Testing
A [pytest](https://docs.pytest.org/en/latest/) suite is provided for testing across multiple Python environments via [tox](https://github.com/tox-dev/tox/):

```bash
$ pipenv run test
```

### Coverage
Test coverage is provided by [pytest-cov](https://github.com/pytest-dev/pytest-cov) via a pipenv script:

```bash
$ pipenv run coverage
```

When running via pipenv, details on missing coverage is provided in the report to allow the user to generate additional tests for full coverage.

e.g.

```
----------- coverage: platform win32, python 3.7.4-final-0 -----------
Name                                Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------
flake8_annotations\__init__.py        108      0     38      0    99%   164
flake8_annotations\checker.py          57      0     30      0   100%
flake8_annotations\enums.py            15      0      0      0   100%
flake8_annotations\error_codes.py      85      0      0      0   100%
-------------------------------------------------------------------------------
TOTAL                                 265      0     68      0    99%
```
