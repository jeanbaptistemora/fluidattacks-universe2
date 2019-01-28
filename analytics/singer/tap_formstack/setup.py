"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_formstack",
    version="1.0.0",
    description="Singer tap for the Formstack API",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        tap-formstack=tap_formstack:main
    """,

    packages=[
        "tap_formstack"
    ],
)
