"""Package setup file.
"""

import os
import setuptools


def read(fname: str) -> str:
    """Read a file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="tap_git",
    version="1.0.0",
    description="Singer tap for a git repository",

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    long_description=read("README.md"),
    python_requires=">3.6",

    license="GPL",
    keywords="git",
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
        "gitpython==3.0.8"
    ],

    entry_points="""
        [console_scripts]
        tap-git=tap_git:main
    """,

    packages=[
        "tap_git"
    ],

    package_data={
        "tap_git": [
            "commits.schema.json",
            "changes.schema.json",
            "gitinspector_blame.schema.json",
            "gitinspector_changes.schema.json",
            "gitinspector_metrics.schema.json",
            "gitinspector_responsibilities.schema.json",
            "metrics_lines_per_actor.schema.json",
            "metrics_median_line_age.schema.json",
        ]
    },
)
