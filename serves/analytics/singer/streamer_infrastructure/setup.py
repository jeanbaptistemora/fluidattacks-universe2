"""Package setup file."""

import os
import setuptools


def read(fname: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="streamer_infrastructure",
    version="1.0.0",
    description="Streamer for the Fluid Infrastructure",

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    long_description=read("README.md"),
    python_requires=">3.6",

    license="BSD",
    keywords="Infrastructure",
    author_email="kamado@fluidattacks.com",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=True,

    install_requires=[
        "boto3"
    ],

    entry_points="""
        [console_scripts]
        streamer-infrastructure=streamer_infrastructure:main
    """,

    packages=[
        "streamer_infrastructure"
    ],
)
