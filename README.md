# flake8-type-hinted
[![Discord](https://discordapp.com/api/guilds/267624335836053506/embed.png)](https://discord.gg/2B963hn)

`flake8-annotations` is a plugin for Flake8 for detecting when variables and/or return annotations are missing type annotations in function and method definitions.

What this won't do: Check for variable type annotations.

## Alpha Warning
This package is currently in an alpha state, it's *highly* recommended that this be installed in a virtual environment.

Per-warning ignore configuration via CLI, `.flake8`, or similar is currently unsupported.

## Installation

With the repository cloned and inside an activated virtual environment:

```bash
$ pip install .
```

## Table of Warnings
### Function Annotations
| ID     | Description                                   |
|--------|-----------------------------------------------|
| TYP001 | Missing type annotation for function argument |
| TYP002 | Missing type annotation for `*args`           |
| TYP003 | Missing type annotation for `**kwargs`        |

### Method Annotations
| ID     | Description                                        |
|--------|----------------------------------------------------|
| TYP101 | Missing type annotation for `self` in class method |
| TYP102 | Missing type annotation for `cls` in classmethod   |

### Return Annotations
| ID     | Description                                         |
|--------|-----------------------------------------------------|
| TYP201 | Missing return type annotation for public method    |
| TYP202 | Missing return type annotation for protected method |
| TYP203 | Missing return type annotation for secret method    |
| TYP204 | Missing return type annotation for magic method     |
| TYP205 | Missing return type annotation for staticmethod     |
| TYP206 | Missing return type annotation for classmethod      |