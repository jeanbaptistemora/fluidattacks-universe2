# -*- coding: utf-8 -*-

"""Installation script.

This module defines the minimum requirements to generate an standard
setup script of fluidasserts.
"""

import io
import time
from setuptools import setup


def _get_readme():
    """Return fluidasserts readme."""
    readme_path = 'build/config/README.rst'
    with io.open(readme_path, 'rt', encoding='utf8') as readme_f:
        return readme_f.read()


def _get_version():
    """Return fluidasserts version."""
    cur_time = time.gmtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime(f'%y.%m.{min_month}')


def _get_requirements():
    """Return fluidasserts requirements."""
    with open('requirements.txt') as file:
        return [line.strip() for line in file]


setup(
    name='fluidasserts',
    description='Assertion Library for Security Assumptions',
    long_description=_get_readme(),
    long_description_content_type='text/x-rst',
    version=_get_version(),
    url='https://fluidattacks.com/web/products/asserts',
    project_urls={
        'Documentation': 'https://fluidattacks.gitlab.io/asserts/',
    },
    package_dir={
        'fluidasserts': 'fluidasserts',
    },
    author='Fluid Attacks Engineering Team',
    author_email='engineering@fluidattacks.com',
    packages=[
        'fluidasserts',
        'fluidasserts.cloud',
        'fluidasserts.cloud.aws',
        'fluidasserts.cloud.aws.cloudformation',
        'fluidasserts.cloud.aws.terraform',
        'fluidasserts.db',
        'fluidasserts.format',
        'fluidasserts.helper',
        'fluidasserts.iot',
        'fluidasserts.lang',
        'fluidasserts.ot',
        'fluidasserts.proto',
        'fluidasserts.sca',
        'fluidasserts.syst',
        'fluidasserts.utils',
    ],
    classifiers=[
        'Environment :: Console',
        'Topic :: Security',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
    ],
    install_requires=_get_requirements(),
    include_package_data=True,         # files to include in MANIFEST.in
    entry_points={
        'console_scripts': [
            'asserts=fluidasserts.utils.cli:main',
        ],
    },
)
