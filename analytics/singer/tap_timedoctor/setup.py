"""
package setup file
"""

import setuptools

setuptools.setup(
    name='tap_timedoctor',
    version='1.0.0',
    description='Singer.io tap for the Time Doctor API',
    classifiers=['Programming Language :: Python :: 3 :: Only'],

    author='Fluid Attacks, We hack your software.',
    url='https://fluidattacks.com/',

    py_modules=[],

    install_requires=[],

    entry_points='''
        [console_scripts]
        tap_timedoctor=tap_timedoctor:main
    ''',

    packages=['tap_timedoctor'],
)
