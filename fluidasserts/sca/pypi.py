# -*- coding: utf-8 -*-

"""Software Composition Analysis for Python packages."""

# standard imports
# None

# 3rd party imports
from requirements_detector import find_requirements
from requirements_detector.detect import RequirementsNotFound

# local imports
from fluidasserts.helper import sca
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify

PACKAGE_MANAGER = 'pypi'


def _get_requirements(path: str) -> list:
    """
    Get list of requirements from Python project.

    Files supported are setup.py and requirements.txt

    :param path: Project path
    """
    _reqs = ((x.name, x.version_specs) for x in find_requirements(path))
    reqs = []
    for req in _reqs:
        if req[1]:
            reqs.append((req[0], req[1][0][1]))
        else:
            reqs.append((req[0], None))
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
    except (FileNotFoundError, RequirementsNotFound):
        show_unknown('Project dir not found',
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
