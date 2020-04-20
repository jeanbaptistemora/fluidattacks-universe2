"""Setup package."""

# Standard imports
from datetime import datetime

try:
    import distutils.core
except ImportError:
    import distutils


def get_minor_version() -> int:
    """Number of seconds since the beginning of the month."""
    utc_now = \
        datetime.utcnow()
    utc_beginning_of_month = \
        datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    return int((utc_now - utc_beginning_of_month).total_seconds())


def get_version():
    """Return the package version."""
    return datetime.utcnow().strftime(f'%Y.%m.{get_minor_version()}')


def get_extras_require():
    extras_require = {
        'with_asserts': [
            'fluidasserts',
        ],
    }
    extras_require['with_everything'] = [
        extra_requirement
        for extra_requirements in extras_require.values()
        for extra_requirement in extra_requirements
    ]
    return extras_require


def get_install_requires():
    with open('requirements.txt') as requirements_handle:
        return requirements_handle.readlines()


distutils.core.setup(
    name='fluidattacks',
    version=get_version(),
    description='Fluid Attacks Toolkit and SDK',
    author='Fluid Attacks',
    author_email='engineering@fluidattacks.com',
    packages=[
        'toolbox',
        'toolbox.analytics',
        'toolbox.api',
        'toolbox.cli',
        'toolbox.drills',
        'toolbox.forces',
        'toolbox.generic',
        'toolbox.helper',
        'toolbox.sorts',
        'toolbox.utils',
    ],
    install_requires=get_install_requires(),
    extras_require=get_extras_require(),
    entry_points={
        'console_scripts': [
            'fluid=toolbox.cli:main'
        ],
    },
    include_package_data=True,
)
