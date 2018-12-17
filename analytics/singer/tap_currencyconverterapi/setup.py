"""
package setup file
"""

import setuptools

setuptools.setup(
    name='tap_currencyconverterapi',
    version='1.0.0',
    description='Singer.io tap for the https://www.currencyconverterapi.com/ API',
    classifiers=['Programming Language :: Python :: 3 :: Only'],

    author='Fluid Attacks, We hack your software.',
    url='https://fluidattacks.com/',

    py_modules=[],

    install_requires=[],

    entry_points='''
        [console_scripts]
        tap_currencyconverterapi=tap_currencyconverterapi:main
    ''',

    packages=['tap_currencyconverterapi'],
)
