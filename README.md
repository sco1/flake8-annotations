# flake8-annotations
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations)
![PyPI](https://img.shields.io/pypi/v/flake8-annotations)
[![Discord](https://discordapp.com/api/guilds/267624335836053506/embed.png)](https://discord.gg/2B963hn)


`flake8-annotations` is a plugin for Flake8 for detecting when variables and/or return type annotations are missing in function and method definitions.

What this won't do: Check for variable type annotations.

## Alpha Warning
This package is currently in an alpha state, it's *highly* recommended that this be installed in a virtual environment.

## Installation

Install directly from PyPi inside an activated virtual environment with your favorite `pip` invocation:

```bash
$ pip install flake8-annotations
```

For development, you can also install from source as editable inside an activated virtual environment:

```bash
$ pip install -e .
```

## Table of Warnings
### Function Annotations
| ID       | Description                                   |
|----------|-----------------------------------------------|
| `TYP001` | Missing type annotation for function argument |
| `TYP002` | Missing type annotation for `*args`           |
| `TYP003` | Missing type annotation for `**kwargs`        |

### Method Annotations
| ID       | Description                                           |
|----------|-------------------------------------------------------|
| `TYP101` | Missing type annotation for `self` in class method    |
| `TYP102` | Missing type annotation for `self` in property method |
| `TYP103` | Missing type annotation for `cls` in classmethod      |

### Return Annotations
| ID       | Description                                           |
|----------|-------------------------------------------------------|
| `TYP201` | Missing return type annotation for public function    |
| `TYP202` | Missing return type annotation for protected function |
| `TYP203` | Missing return type annotation for secret function    |
| `TYP204` | Missing return type annotation for special method     |
| `TYP205` | Missing return type annotation for staticmethod       |
| `TYP206` | Missing return type annotation for classmethod        |
| `TYP207` | Missing return type annotation for class property     |
