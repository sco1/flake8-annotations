# flake8-annotations
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations)
![PyPI](https://img.shields.io/pypi/v/flake8-annotations)
[![Build Status](https://dev.azure.com/python-discord/Python%20Discord/_apis/build/status/python-discord.flake8-annotations?branchName=master)](https://dev.azure.com/python-discord/Python%20Discord/_build/latest?definitionId=16&branchName=master)
[![Discord](https://discordapp.com/api/guilds/267624335836053506/embed.png)](https://discord.gg/2B963hn)


`flake8-annotations` is a plugin for [Flake8](http://flake8.pycqa.org/en/latest/) that detects when arguments and/or return [type annotations](https://www.python.org/dev/peps/pep-0484/) are missing in function and method definitions.

What this won't do: Check variable annotations, compile-time type checking (see: [mypy](http://mypy-lang.org/))

## Installation

Install from PyPi with your favorite `pip` invocation:

```bash
$ pip install flake8-annotations
```

It will then be run automatically as part of Flake8.

You can verify it's being picked up by invoking the following in your shell:

```bash
$ flake8 --version
3.7.8 (flake8-annotations: 1.0.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.7.4 on Darwin
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

## Contributing
Please take some time to read through our [contributing guidelines](CONTRIBUTING.md) before helping us with this project.

### Development Environment
This project uses [Pipenv](https://docs.pipenv.org/en/latest/) to manage dependencies. With your fork cloned to your local machine, you can create a developer environment using:

```bash
$ pipenv sync --dev
```

A [pre-commit](https://pre-commit.com) installation script and configuration is also provided to create a pre-commit hook so linting errors aren't committed:

```bash
$ pipenv run precommit
```

### Testing
A [pytest](https://docs.pytest.org/en/latest/) suite is provided for testing:

```bash
$ pipenv run test
```