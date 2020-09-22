"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_gitlab",
    version="0.0.1",
    description="Singer tap for gitlab",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        tap-gitlab=tap_gitlab:main
    """,

    packages=[
        "tap_gitlab"
    ],
)
