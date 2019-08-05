from setuptools import find_packages, setup
import sys

assert sys.version_info >= (3, 6, 0), "ast-adventures requires Python 3.6+"

setup(
    name="ast_adventures",
    license="MIT",
    version="2019.0",
    description="Experimental Framework for Flake8 Type Hint Enforcement",
    author="Python Discord",
    author_email="staff@pythondiscord.com",
    url="https://github.com/python-discord/ast-adventures",
    packages=find_packages(),
    entry_points={
        "flake8_extension": [
            'TYP = ast_adventures.checker:TypeHintChecker',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    install_requires=[
        "flake8>=3.7,<3.8"
    ],
    extras_require={
        "dev": [
            "flake8-bugbear",
            "flake8-docstrings"
            "flake8-import-order",
            "flake8-string-format",
            "flake8-tidy-imports",
            "flake8-todo",
            "pre-commit",
        ]
    }
)