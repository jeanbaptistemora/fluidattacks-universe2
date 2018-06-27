# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.sca packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.sca import bower
from fluidasserts.sca import chocolatey
from fluidasserts.sca import maven
from fluidasserts.sca import npm
from fluidasserts.sca import nuget
from fluidasserts.sca import pypi


# Constants
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


#
# Open tests
#


def test_package_has_vulnerabilities_open():
    """Search vulnerabilities."""
    assert bower.package_has_vulnerabilities('jquery')
    assert chocolatey.package_has_vulnerabilities('python')
    assert maven.package_has_vulnerabilities('maven')
    assert maven.project_has_vulnerabilities(MAVEN_PROJECT_OPEN)
    assert npm.package_has_vulnerabilities('npm')
    assert nuget.package_has_vulnerabilities('jquery')
    assert nuget.project_has_vulnerabilities(NUGET_PROJECT_OPEN)
    assert pypi.package_has_vulnerabilities('pip')
    assert pypi.project_has_vulnerabilities(PYPI_PROJECT_OPEN)



#
# Closing tests
#

def test_package_has_vulnerabilities_close():
    """Search vulnerabilities."""
    assert not bower.package_has_vulnerabilities('jquery', '3.0.0')
    assert not bower.package_has_vulnerabilities('jqueryasudhaiusd', '3.0.0')
    assert not chocolatey.package_has_vulnerabilities('python', '3.7.0')
    assert not chocolatey.package_has_vulnerabilities('jqueryasudhai', '3.7')
    assert not maven.package_has_vulnerabilities('maven', '5.0.0')
    assert not maven.package_has_vulnerabilities('mavenasdasda', '5.0.0')
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_CLOSE)
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_NOT_FOUND)
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_EMPTY)
    assert not npm.package_has_vulnerabilities('npm', '10.0.0')
    assert not npm.package_has_vulnerabilities('npasdasdasm', '10.0.0')
    assert not nuget.package_has_vulnerabilities('jquery', '10.0.0')
    assert not nuget.package_has_vulnerabilities('jqueryasdasd', '10.0.0')
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_CLOSE)
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_NOT_FOUND)
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_EMPTY)
    assert not pypi.package_has_vulnerabilities('pips')
    assert not pypi.package_has_vulnerabilities('pipasdiahsds')
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_CLOSE)
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_NOT_FOUND)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'
    assert not bower.package_has_vulnerabilities('jquery')
    assert not chocolatey.package_has_vulnerabilities('python')
    assert not maven.package_has_vulnerabilities('maven')
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_CLOSE)
    assert not maven.project_has_vulnerabilities(MAVEN_PROJECT_CLOSE)
    assert not npm.package_has_vulnerabilities('npm')
    assert not nuget.package_has_vulnerabilities('jquery')
    assert not nuget.project_has_vulnerabilities(NUGET_PROJECT_CLOSE)
    assert not pypi.package_has_vulnerabilities('pip')
    assert not pypi.project_has_vulnerabilities(PYPI_PROJECT_CLOSE)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)