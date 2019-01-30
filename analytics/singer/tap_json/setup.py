"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_json",
    version="1.0.0",
    description="Singer tap for a JSON stream",

    author="Fluid Attacks; We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
    ],

    entry_points="""
        [console_scripts]
        tap-json=tap_json:main
    """,

    packages=[
        "tap_json"
    ],
)
