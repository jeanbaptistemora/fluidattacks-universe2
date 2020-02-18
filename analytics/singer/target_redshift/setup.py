"""Package setup file."""

import os
import setuptools


def read(fname: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    version="1.0.0",
    name="target_redshift",
    url="https://fluidattacks.com/",

    author="Fluid Attacks",
    author_email="kamado@fluidattacks.com",
    maintainer="Kevin Amado",
    maintainer_email="kamado@fluidattacks.com",

    description="Singer target for Amazon Redshift",
    long_description=read("README.md"),

    python_requires=">=3.6",

    install_requires=[
        "jsonschema==3.2.0",
        "psycopg2==2.8.4"
    ],

    entry_points="""
        [console_scripts]
        target-redshift=target_redshift:main
    """,

    packages=[
        "target_redshift"
    ],

    py_modules=[
    ],

    license="GPL",
    keywords="Infrastructure",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False,
)
