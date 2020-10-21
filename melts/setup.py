"""Setup package."""

# Standard imports
import os
from distutils import dist
from datetime import datetime

try:
    import distutils.core
except ImportError:
    import distutils

PKG_NAME = "melts"


def get_minor_version() -> int:
    """Number of seconds since the beginning of the month."""
    utc_now = \
        datetime.utcnow()
    utc_beginning_of_month = \
        datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    return int((utc_now - utc_beginning_of_month).total_seconds())


def get_version():
    """Return the package version."""
    metadata_file = "PKG-INFO"
    if os.path.exists(metadata_file):
        pkg_metadata = dist.DistributionMetadata(metadata_file)
        return pkg_metadata.get_version()

    return datetime.utcnow().strftime(f'%Y.%m.{get_minor_version()}')


def get_install_requires():
    with open('requirements.txt') as requirements_handle:
        return requirements_handle.readlines()


distutils.core.setup(
    name=PKG_NAME,
    version=get_version(),
    description='Fluid Attacks Toolkit and SDK',
    author='Fluid Attacks',
    author_email='engineering@fluidattacks.com',
    packages=[
        'toolbox',
        'toolbox.api',
        'toolbox.cli',
        'toolbox.drills',
        'toolbox.forces',
        'toolbox.generic',
        'toolbox.utils',
        'toolbox.reports'
    ],
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'melts=toolbox.cli:main'
        ],
    },
    include_package_data=True,
)
