# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.sca packages."""

# standard imports
import os
import contextlib

# 3rd party imports
# None

# local imports
from fluidasserts.sca import bower
from fluidasserts.sca import chocolatey
from fluidasserts.sca import maven
from fluidasserts.sca import npm
from fluidasserts.sca import nuget
from fluidasserts.sca import pypi
from fluidasserts.sca import linux
from fluidasserts.sca import rubygems

# Constants
PROJECT = 'test/static/sca'
MAVEN_PROJECT_OPEN = 'test/static/sca/maven/open'
MAVEN_PROJECT_CLOSE = 'test/static/sca/maven/close'
MAVEN_PROJECT_NOT_FOUND = 'test/static/sca/maven/not_found'
MAVEN_PROJECT_EMPTY = 'test/static/sca/maven/empty'
NUGET_PROJECT_OPEN = 'test/static/sca/nuget/open'
NUGET_PROJECT_CLOSE = 'test/static/sca/nuget/close'
NUGET_PROJECT_NOT_FOUND = 'test/static/sca/nuget/not_found'
NUGET_PROJECT_EMPTY = 'test/static/sca/nuget/empty'
PYPI_PROJECT_OPEN = 'test/static/sca/pypi/open'
PYPI_PROJECT_CLOSE = 'test/static/sca/pypi/close'
PYPI_PROJECT_NOT_FOUND = 'test/static/sca/pypi/not_found'
PYPI_PROJECT_EMPTY = 'test/static/sca/pypi/empty'
NPM_PROJECT_OPEN = 'test/static/sca/npm/open'
NPM_PROJECT_CLOSE = 'test/static/sca/npm/close'
NPM_PROJECT_NOT_FOUND = 'test/static/sca/npm/not_found'
NPM_PROJECT_EMPTY = 'test/static/sca/npm/empty'


@contextlib.contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)


#
# Open tests
#


def test_bower_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert bower.package_has_vulnerabilities('jquery')


def test_chocolatey_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert chocolatey.package_has_vulnerabilities('python')


def test_maven_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert maven.package_has_vulnerabilities('maven')
    assert maven.project_has_vulnerabilities(MAVEN_PROJECT_OPEN)


def test_npm_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert npm.package_has_vulnerabilities('jquery')
    assert npm.project_has_vulnerabilities(NPM_PROJECT_OPEN)


def test_nuget_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert nuget.package_has_vulnerabilities('jquery')
    assert nuget.project_has_vulnerabilities(NUGET_PROJECT_OPEN)


def test_pypi_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert pypi.package_has_vulnerabilities('django')
    assert pypi.project_has_vulnerabilities(PYPI_PROJECT_OPEN)


#
# Closing tests
#


def test_bower_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not bower.package_has_vulnerabilities('jquery', '3.0.0')
    assert not bower.package_has_vulnerabilities('jqueryasudhaiusd', '3.0.0')

    with no_connection():
        assert not bower.package_has_vulnerabilities('jquery', retry=False)


def test_chocolatey_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not chocolatey.package_has_vulnerabilities('python', '3.7.0')
    assert not chocolatey.package_has_vulnerabilities('jqueryasudhai', '3.7')

    with no_connection():
        assert not chocolatey.package_has_vulnerabilities(
            'python', retry=False)


def test_maven_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not maven.package_has_vulnerabilities('maven', '5.0.0')
    assert not maven.package_has_vulnerabilities('mavenasdasda', '5.0.0')
    assert not maven.project_has_vulnerabilities(PROJECT, exclude=['test'])
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_CLOSE)
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_NOT_FOUND)
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_EMPTY)

    with no_connection():
        assert not maven.package_has_vulnerabilities('maven', retry=False)
        assert not maven.project_has_vulnerabilities(
            MAVEN_PROJECT_CLOSE, retry=False)


def test_npm_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not npm.package_has_vulnerabilities('extend', '10.0.0')
    assert not npm.package_has_vulnerabilities('npasdasdasm', '10.0.0')
    assert not npm.project_has_vulnerabilities(PROJECT, exclude=['test'])
    assert not npm.project_has_vulnerabilities(NPM_PROJECT_CLOSE)
    assert not npm.project_has_vulnerabilities(NPM_PROJECT_NOT_FOUND)
    assert not npm.project_has_vulnerabilities(NPM_PROJECT_EMPTY)

    with no_connection():
        assert not npm.package_has_vulnerabilities('extend', retry=False)
        assert not npm.project_has_vulnerabilities(
            NPM_PROJECT_CLOSE, retry=False)


def test_nuget_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not nuget.package_has_vulnerabilities('jquery', '10.0.0')
    assert not nuget.package_has_vulnerabilities('jqueryasdasd', '10.0.0')
    assert not nuget.project_has_vulnerabilities(PROJECT, exclude=['test'])
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_CLOSE)
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_NOT_FOUND)
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_EMPTY)

    with no_connection():
        assert not nuget.package_has_vulnerabilities('jquery', retry=False)
        assert not nuget.project_has_vulnerabilities(
            NUGET_PROJECT_CLOSE, retry=False)


def test_pypi_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not pypi.package_has_vulnerabilities('pips')
    assert not pypi.package_has_vulnerabilities('pipasdiahsds')
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_CLOSE)
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_NOT_FOUND)
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_EMPTY)

    with no_connection():
        assert not pypi.package_has_vulnerabilities('pip', retry=False)
        assert not pypi.project_has_vulnerabilities(
            PYPI_PROJECT_CLOSE, retry=False)


def test_linux_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not linux.package_has_vulnerabilities('jquery')

    with no_connection():
        assert not linux.package_has_vulnerabilities('jquery', retry=False)


def test_rubygems_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not rubygems.package_has_vulnerabilities('jquery-rails', '5.0.0')

    with no_connection():
        assert not rubygems.package_has_vulnerabilities(
            'jquery-rails', retry=False)
