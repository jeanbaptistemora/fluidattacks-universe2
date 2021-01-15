"""Setup package."""

# Standard imports
import os
from distutils import dist
from datetime import datetime
from typing import List

try:
    import distutils.core
except ImportError:
    import distutils

PKG_NAME = "melts"


def get_minor_version() -> int:
    """Number of seconds since the beginning of the month."""
    utc_now = datetime.utcnow()
    utc_beginning_of_month = datetime.utcnow().replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return int((utc_now - utc_beginning_of_month).total_seconds())


def get_version() -> str:
    """Return the package version."""
    metadata_file = "PKG-INFO"
    if os.path.exists(metadata_file):
        pkg_metadata = dist.DistributionMetadata(metadata_file)  # type:ignore
        return pkg_metadata.get_version()

    return datetime.utcnow().strftime(f'%Y.%m.{get_minor_version()}')


def get_install_requires() -> List[str]:
    with open('requirements.txt') as requirements_handle:
        return requirements_handle.readlines()


def get_long_description() -> str:
    long_description = ""
    with open('README.md', encoding='utf-8') as readme_file:
        long_description = readme_file.read()
    return long_description


distutils.core.setup(
    name=PKG_NAME,
    version=get_version(),
    description='Fluid Attacks Toolkit and SDK',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Fluid Attacks',
    author_email='engineering@fluidattacks.com',
    packages=[
        'toolbox',
        'toolbox.api',
        'toolbox.cli',
        'toolbox.drills',
        'toolbox.generic',
        'toolbox.utils',
    ],
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'melts=toolbox.cli:main'
        ],
    },
    include_package_data=True,
)
