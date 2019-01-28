"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_awsdynamodb",
    version="1.0.0",
    description="Singer tap for Amazon Web Services's DynamoDB",
    classifiers=["Programming Language :: Python :: 3 :: Only"],

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
        "boto3"
    ],

    entry_points="""
        [console_scripts]
        tap-awsdynamodb=tap_awsdynamodb:main
    """,

    packages=[
        "tap_awsdynamodb"
    ],
)
