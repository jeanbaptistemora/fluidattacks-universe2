"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_git",
    version="1.0.0",
    description="Singer tap for a git repository",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
        "gitpython"
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
            "changes.schema.json"
        ]
    },
)
