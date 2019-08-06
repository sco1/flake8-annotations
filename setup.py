import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 6, 0), "flake8-annotations requires Python 3.6+"

setup(
    name="flake8_annotations",
    license="MIT",
    version="2019.0",
    description="Flake8 Type Annotation Checks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Python Discord",
    author_email="staff@pythondiscord.com",
    url="https://github.com/python-discord/flake8-annotations",
    packages=find_packages(),
    entry_points={
        "flake8.extension": [
            'TYP = flake8_annotations.checker:TypeHintChecker',
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
        "flake8~=3.7.8"
    ],
    extras_require={
        "dev": [
            "flake8-bugbear~=19.3",
            "flake8-docstrings~=1.3",
            "flake8-import-order~=0.18",
            "flake8-string-format~=0.2",
            "flake8-tidy-imports~=2.0",
            "flake8-todo~=0.7",
        ]
    }
)
