# -*- coding: utf-8 -*-

"""Software Composition Analysis for NuGet (C#) packages."""

# standard imports
# None

# 3rd party imports
from defusedxml.ElementTree import parse

# local imports
from fluidasserts.helper import sca
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import track, level, notify

PACKAGE_MANAGER = 'nuget'


def _get_requirements(path: str) -> list:
    """
    Get list of requirements from NuGet project.

    Files supported are packages.config

    :param path: Project path
    """
    reqs = []
    for full_path in get_paths(path, endswith=('packages.config',)):
        tree = parse(full_path)
        deps = tree.findall(".//package")
        reqs += [(dep.attrib['id'], dep.attrib['version']) for dep in deps]
    return reqs


@notify
@level('high')
@track
def package_has_vulnerabilities(package: str, version: str = None) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    return sca.get_vulns_from_ossindex(PACKAGE_MANAGER, package, version)


@notify
@level('high')
@track
def project_has_vulnerabilities(path: str) -> bool:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    """
    try:
        reqs = _get_requirements(path)
    except FileNotFoundError:
        show_unknown('Project dir not found',
                     details=dict(path=path))
        return False

    if not reqs:
        show_unknown('Not packages found in project',
                     details=dict(path=path))
        return False

    result = True
    try:
        unfiltered = {f'{x[0]} {x[1]}':
                      sca.get_vulns_ossindex(PACKAGE_MANAGER, x[0], x[1])
                      for x in reqs}
        proj_vulns = {k: v for k, v in unfiltered.items() if v}
    except sca.ConnError as exc:
        show_unknown('Could not connect to SCA provider',
                     details=dict(error=str(exc).replace(':', ',')))
        result = False
    else:
        if proj_vulns:
            show_open('Project has dependencies with vulnerabilities',
                      details=dict(project_path=path,
                                   vulnerabilities=proj_vulns))
            result = True
        else:
            show_close('Project has not dependencies with vulnerabilities',
                       details=dict(project_path=path))
            result = False
    return result
