"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_csv",
    version="1.0.0",
    description="Singer tap for a CSV file",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[],

    install_requires=[],

    entry_points="""
        [console_scripts]
        tap-csv=tap_csv:main
    """,

    packages=["tap_csv"],
)
