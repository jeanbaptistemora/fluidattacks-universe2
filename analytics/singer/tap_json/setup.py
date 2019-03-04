#!/usr/bin/env python3
"""Package setup file."""

import os
import setuptools


def read(file_name: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setuptools.setup(
    version="1.0.0",
    name="tap_json",
    url="https://fluidattacks.com/",

    author="Fluid Attacks",
    author_email="kamado@fluidattacks.com",
    maintainer="Kevin Amado",
    maintainer_email="kamado@fluidattacks.com",

    description="Singer tap for a generic JSON stream.",
    long_description=read("README.md"),

    python_requires=">=3.7",

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        tap-json=tap_json:main
    """,

    packages=[
        "tap_json"
    ],

    py_modules=[
    ],

    license="GPL",
    keywords="JSON",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False,
)
