"""Package setup file.
"""

import setuptools

setuptools.setup(
    name="streamer_mandrill",
    version="1.0.0",
    description="Streamer for the mandrill API",

    author="Fluid Attacks, We hack your software.",
    url="https://fluidattacks.com/",

    py_modules=[
    ],

    install_requires=[
        "mandrill-really-maintained"
    ],

    entry_points="""
        [console_scripts]
        streamer-mandrill=streamer_mandrill:main
    """,

    packages=["streamer_mandrill"],
)
