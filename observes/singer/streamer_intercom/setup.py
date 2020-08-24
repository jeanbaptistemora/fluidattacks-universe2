"""Package setup file."""

import os
import setuptools


def read(fname: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    version="1.0.0",
    name="streamer_intercom",
    url="https://fluidattacks.com/",

    author="Fluid Attacks",
    author_email="kamado@fluidattacks.com",

    maintainer="Kevin Amado",
    maintainer_email="kamado@fluidattacks.com",

    description="Streamer for the Intercom API",
    long_description=read("README.md"),

    python_requires=">=3.6",

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        streamer-intercom=streamer_intercom:main
    """,

    packages=[
        "streamer_intercom"
    ],

    py_modules=[
    ],

    license="GPL",
    keywords="Intercom",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False,
)
