"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_timedoctor",
    version="1.0.0",
    description="Singer tap for the Time Doctor API",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        tap-timedoctor=tap_timedoctor:main
    """,

    packages=[
        "tap_timedoctor"
    ],
)
