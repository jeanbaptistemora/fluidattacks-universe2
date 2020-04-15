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


_EXTRAS_REQUIRE = {
    'with_asserts': [
        'fluidasserts',
    ],
}
_EXTRAS_REQUIRE['with_everything'] = [
    extra_requirement
    for extra_requirements in _EXTRAS_REQUIRE.values()
    for extra_requirement in extra_requirements
]

distutils.core.setup(
    name='continuous-toolbox',
    version=get_version(),
    description='Continuous Toolbox',
    author='Fluid Attacks',
    author_email='engineering@fluidattacks.com',
    packages=[
        'toolbox',
        'toolbox.analytics',
        'toolbox.api',
        'toolbox.forces',
        'toolbox.helper',
    ],
    install_requires=[
        'awscli==1.17.9',
        'binaryornot==0.4.4',
        'frozendict==1.2',
        'okta-awscli==0.4.0',
        'pandas==1.0.3',
        'progress==1.5',
        'prospector[with_everything]==1.2.0',
        'pydriller==1.13',
        'pynamodb==4.3.1',
        'pykwalify==1.7.0',
        'python-dateutil==2.8.1',
        'python-jose==3.0.1',
        'requests==2.22.0',
        'ruamel.yaml==0.16.5',
        'simplejson==3.16.0',
        'mandrill-really-maintained==1.2.4',
    ],
    extras_require=_EXTRAS_REQUIRE,
    entry_points={
        'console_scripts': [
            'toolbox=toolbox.cli:main',
            'fluid=toolbox.new_cli:main'
        ],
    },
    include_package_data=True,
)
