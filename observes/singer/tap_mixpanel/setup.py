"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="tap_mixpanel",
    version="1.0.0",
    description="Singer tap for mixpanel event data",
    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[],

    install_requires=[],

    entry_points="""
        [console_scripts]
        tap-mixpanel=tap_mixpanel:main
    """,

    packages=["tap_mixpanel"],
)
