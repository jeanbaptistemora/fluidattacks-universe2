"""Package setup file."""

import os
import setuptools


def read(fname: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="tap_awsdynamodb",
    version="1.0.0",
    description="Singer tap for Amazon Web Services's DynamoDB",
    url="https://fluidattacks.com/",
    long_description=read("README.md"),

    author="Fluid Attacks",
    author_email="engineering@fluidattacks.com",
    maintainer="Kevin Amado",
    maintainer_email="kamado@fluidattacks.com",

    py_modules=[
    ],

    install_requires=[
        "boto3==1.9.213",
        "python-dateutil==2.8.0",
    ],

    entry_points="""
        [console_scripts]
        tap-awsdynamodb=tap_awsdynamodb:main
    """,

    packages=[
        "tap_awsdynamodb"
    ],


    license="GPL",
    keywords="Formstack",
    classifiers=[
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
