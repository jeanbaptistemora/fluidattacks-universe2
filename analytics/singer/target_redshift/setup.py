"""
package setup file
"""

import setuptools

setuptools.setup(
    name='target_redshift',
    version='1.0.0',
    description='Singer.io target for Amazon Redshift',
    classifiers=['Programming Language :: Python :: 3 :: Only'],

    author='Fluid Attacks, We hack your software.',
    url='https://fluidattacks.com/',

    py_modules=[],

    install_requires=[
        "psycopg2-binary"
    ],

    entry_points='''
        [console_scripts]
        target-redshift=target_redshift:main
    ''',

    packages=['target_redshift'],
)
