# flake8-annotations
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations/3.0.1?logo=python&logoColor=FFD43B)](https://pypi.org/project/flake8-annotations/)
[![PyPI](https://img.shields.io/pypi/v/flake8-annotations?logo=Python&logoColor=FFD43B)](https://pypi.org/project/flake8-annotations/)
[![PyPI - License](https://img.shields.io/pypi/l/flake8-annotations?color=magenta)](https://github.com/sco1/flake8-annotations/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/flake8-annotations/main.svg)](https://results.pre-commit.ci/latest/github/sco1/flake8-annotations/main)
[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://github.dev/sco1/flake8-annotations)

`flake8-annotations` is a plugin for [Flake8](http://flake8.pycqa.org/en/latest/) that detects the absence of [PEP 3107-style](https://www.python.org/dev/peps/pep-3107/) function annotations.

What this won't do: replace [mypy](http://mypy-lang.org/), check type comments (see: [PEP 484](https://peps.python.org/pep-0484/#type-comments)), check variable annotations (see: [PEP 526](https://www.python.org/dev/peps/pep-0526/)), or respect stub files.

## Installation
Install from PyPi with your favorite `pip` invocation:

```bash
$ pip install flake8-annotations
```

It will then be run automatically as part of flake8.

You can verify it's being picked up by invoking the following in your shell:


<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["flake8", "--version"], stdout=PIPE, encoding="ascii")
ver_str = out.stdout.replace("\n", "")
cog.out(
    f"```bash\n$ flake8 --version\n{ver_str}\n```"
)
]]] -->
```bash
$ flake8 --version
6.1.0 (flake8-annotations: 3.0.1, mccabe: 0.7.0, pycodestyle: 2.11.1, pyflakes: 3.1.0) CPython 3.12.0 on Darwin
```
<!-- [[[end]]] -->

## Table of Warnings
With the exception of `ANN4xx`-level warnings, all warnings are enabled by default.

### Function Annotations
| ID       | Description                                   |
|----------|-----------------------------------------------|
| `ANN001` | Missing type annotation for function argument |
| `ANN002` | Missing type annotation for `*args`           |
| `ANN003` | Missing type annotation for `**kwargs`        |

### Method Annotations
| ID       | Description                                                  |
|----------|--------------------------------------------------------------|
| `ANN101` | Missing type annotation for `self` in method<sup>1</sup>     |
| `ANN102` | Missing type annotation for `cls` in classmethod<sup>1</sup> |

### Return Annotations
| ID       | Description                                           |
|----------|-------------------------------------------------------|
| `ANN201` | Missing return type annotation for public function    |
| `ANN202` | Missing return type annotation for protected function |
| `ANN203` | Missing return type annotation for secret function    |
| `ANN204` | Missing return type annotation for special method     |
| `ANN205` | Missing return type annotation for staticmethod       |
| `ANN206` | Missing return type annotation for classmethod        |

### Opinionated Warnings
These warnings are disabled by default.
| ID       | Description                                                             |
|----------|-------------------------------------------------------------------------|
| `ANN401` | Dynamically typed expressions (typing.Any) are disallowed<sup>2,3</sup> |
| `ANN402` | Type comments are disallowed<sup>3</sup>                                |

Use [`extend-select`](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-extend-ignore) to enable opinionated warnings without overriding other implicit configurations<sup>4</sup>.

**Notes:**
1. See: [PEP 484](https://www.python.org/dev/peps/pep-0484/#annotating-instance-and-class-methods) and [PEP 563](https://www.python.org/dev/peps/pep-0563/) for suggestions on annotating `self` and `cls` arguments
2. See: [Dynamic Typing Caveats](#dynamic-typing-caveats)
3. Only function declarations are considered by this plugin; type annotations in function/module bodies are not checked 
4. Common pitfall: the use of [`ignore`](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-ignore) will enable all implicitly disabled warnings

## Configuration Options
Some opinionated flags are provided to tailor the linting errors emitted.

### `--suppress-none-returning`: `bool`
Suppress `ANN200`-level errors for functions that meet one of the following criteria:
  * Contain no `return` statement, or
  * Explicit `return` statement(s) all return `None` (explicitly or implicitly).

Default: `False`

### `--suppress-dummy-args`: `bool`
Suppress `ANN000`-level errors for dummy arguments, defined as `_`.

Default: `False`

### `--allow-untyped-defs`: `bool`
Suppress all errors for dynamically typed functions. A function is considered dynamically typed if it does not contain any type hints.

Default: `False`

### `--allow-untyped-nested`: `bool`
Suppress all errors for dynamically typed nested functions. A function is considered dynamically typed if it does not contain any type hints.

Default: `False`

### `--mypy-init-return`: `bool`
Allow omission of a return type hint for `__init__` if at least one argument is annotated. See [mypy's documentation](https://mypy.readthedocs.io/en/stable/class_basics.html?#annotating-init-methods) for additional details.

Default: `False`

### `--dispatch-decorators`: `list[str]`
Comma-separated list of decorators flake8-annotations should consider as dispatch decorators. Linting errors are suppressed for functions decorated with at least one of these functions.

Decorators are matched based on their attribute name. For example, `"singledispatch"` will match any of the following:
  * `import functools; @functools.singledispatch`
  * `import functools as <alias>; @<alias>.singledispatch`
  * `from functools import singledispatch; @singledispatch`

**NOTE:** Deeper imports, such as `a.b.singledispatch` are not supported.

See: [Generic Functions](#generic-functions) for additional information.

Default: `"singledispatch, singledispatchmethod"`

### `--overload-decorators`: `list[str]`
Comma-separated list of decorators flake8-annotations should consider as [`typing.overload`](https://docs.python.org/3/library/typing.html#typing.overload) decorators.

Decorators are matched based on their attribute name. For example, `"overload"` will match any of the following:
  * `import typing; @typing.overload`
  * `import typing as <alias>; @<alias>.overload`
  * `from typing import overload; @overload`

**NOTE:** Deeper imports, such as `a.b.overload` are not supported.

See: [The `typing.overload` Decorator](#the-typingoverload-decorator) for additional information.

Default: `"overload"`

### `--allow-star-arg-any`
Suppress `ANN401` for dynamically typed `*args` and `**kwargs`.

Default: `False`

## Generic Functions
Per the Python Glossary, a [generic function](https://docs.python.org/3/glossary.html#term-generic-function) is defined as:

> A function composed of multiple functions implementing the same operation for different types. Which implementation should be used during a call is determined by the dispatch algorithm.

In the standard library we have some examples of decorators for implementing these generic functions: [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch) and [`functools.singledispatchmethod`](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod). In the spirit of the purpose of these decorators, errors for missing annotations for functions decorated with at least one of these are ignored.

For example, this code:

```py
import functools

@functools.singledispatch
def foo(a):
    print(a)

@foo.register
def _(a: list) -> None:
    for idx, thing in enumerate(a):
        print(idx, thing)
```

Will not raise any linting errors for `foo`.

Decorator(s) to treat as defining generic functions may be specified by the [`--dispatch-decorators`](#--dispatch-decorators-liststr) configuration option.

## The `typing.overload` Decorator
Per the [`typing`](https://docs.python.org/3/library/typing.html#typing.overload) documentation:

> The `@overload` decorator allows describing functions and methods that support multiple different combinations of argument types. A series of `@overload`-decorated definitions must be followed by exactly one non-`@overload`-decorated definition (for the same function/method).

In the spirit of the purpose of this decorator, errors for missing annotations for non-`@overload`-decorated functions are ignored if they meet this criteria.

For example, this code:

```py
import typing


@typing.overload
def foo(a: int) -> int:
    ...

def foo(a):
    ...
```

Will not raise linting errors for missing annotations for the arguments & return of the non-decorated `foo` definition.

Decorator(s) to treat as `typing.overload` may be specified by the [`--overload-decorators`](#--overload-decorators-liststr) configuration option.

## Dynamic Typing Caveats
Support is only provided for the following patterns:
  * `from typing import any; foo: Any`
  * `import typing; foo: typing.Any`
  * `import typing as <alias>; foo: <alias>.Any`

Nested dynamic types (e.g. `typing.Tuple[typing.Any]`) and redefinition (e.g. `from typing import Any as Foo`) will not be identified.

## Contributing

### Development Environment
This project uses [Poetry](https://python-poetry.org/) to manage dependencies. With your fork cloned to your local machine, you can install the project and its dependencies to create a development environment using:

```bash
$ poetry install
```

Note: An editable installation of `flake8-annotations` in the developer environment is required in order for the plugin to be registered for Flake8. By default, Poetry includes an editable install of the project itself when `poetry install` is invoked.

A [pre-commit](https://pre-commit.com) configuration is also provided to create a pre-commit hook so linting errors aren't committed:

```bash
$ pre-commit install
```

### Testing & Coverage
A [pytest](https://docs.pytest.org/en/latest/) suite is provided, with coverage reporting from [pytest-cov](https://github.com/pytest-dev/pytest-cov). A [tox](https://github.com/tox-dev/tox/) configuration is provided to test across all supported versions of Python. Testing will be skipped for Python versions that cannot be found.

```bash
$ tox
```

Details on missing coverage, including in the test suite, is provided in the report to allow the user to generate additional tests for full coverage.
