# Contributing
## Python Version Support
A best attempt is made to support Python versions until they reach EOL, after which support will be formally dropped by the next minor or major release of this package, whichever arrives first. The status of Python versions can be found [here](https://devguide.python.org/versions/).

## Development Environment

Development of this project is done using the supported Python version most recently released. Note that tests are run against all supported versions of Python; see: [Testing & Coverage](#testing--coverage) for additional information.

This project uses [uv](https://docs.astral.sh/uv) to manage dependencies. With your fork cloned to your local machine, you can install the project and its dependencies to create a development environment using:

```text
$ uv venv
$ uv sync --all-extras --dev
```

A [`pre-commit`](https://pre-commit.com) configuration is also provided to create a pre-commit hook so linting errors aren't committed:

```text
$ pre-commit install
```

[`mypy`](https://mypy-lang.org/) is also used by this project to provide static type checking. It can be invoked using:

```text
$ mypy .
```

Note that `mypy` is not included as a pre-commit hook.

## Testing & Coverage

A [pytest](https://docs.pytest.org/en/latest/) suite is provided, with coverage reporting from [`pytest-cov`](https://github.com/pytest-dev/pytest-cov). A [`tox`](https://github.com/tox-dev/tox/) configuration is provided to test across all supported versions of Python. Testing will be skipped locally for Python versions that cannot be found; all supported versions are tested in CI.

```text
$ tox
```

Details on missing coverage, including in the test suite, is provided in the report to allow the user to generate additional tests for full coverage. Full code coverage is expected for the majority of code contributed to this project. Some exceptions are expected, primarily around code whose functionality relies on either user input or the presence of external drives; these interactions are currently not mocked, though this may change in the future.
