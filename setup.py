#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

from etl import __version__

requirements = ["click==7.1.2", "h5py>=3.2.1", "numpy>=1.20.1", "pandas>=1.2.3", "typing>=3.6.2"]
test_requirements = ["coverage", "pytest", "pytest-cov"]


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args.split("|"))
        sys.exit(errno)


setup(
    name="image-etl",
    version=__version__,
    description="CLI tool to extract, transform and load image data.",
    long_description=open("README.md").read(),
    url="https://github.com/darshikaf/image-etl/",
    author="darshikaf",
    author_email="darshikaf@company.com.au",
    keywords="cli",
    packages=find_packages(include=["etl"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=requirements,
    entry_points={"console_scripts": ["etl = etl.cli:main"]},
    test_suite="tests",
    tests_require=test_requirements,
    cmdclass={"test": PyTest},
)
