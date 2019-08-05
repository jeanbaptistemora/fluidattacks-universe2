# -*- coding: utf-8 -*-

"""Software Composition Analysis for Python packages."""

# standard imports
import os

# 3rd party imports
from requirements_detector import find_requirements
from requirements_detector.detect import RequirementsNotFound

# local imports
from fluidasserts import Result
from fluidasserts import HIGH
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_dir_paths
from fluidasserts.utils.decorators import api

PKG_MNGR = 'pypi'


def _get_requirements(path: str, exclude: tuple) -> set:
    """
    Get list of requirements from Python project.

    Files supported are package.json and package-lock.json

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = set()
    if not os.path.exists(path):
        return reqs
    for full_path in get_dir_paths(path, exclude=exclude):
        try:
            reqs.update(
                (req.location_defined,
                 req.name,
                 req.version_specs[0][1] if req.version_specs else None)
                for req in find_requirements(full_path))
        except RequirementsNotFound:
            pass
    return reqs


@api(risk=HIGH)
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> Result:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)


@api(risk=HIGH)
def project_has_vulnerabilities(
        path: str, exclude: list = None, retry: bool = True) -> Result:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    exclude = tuple(exclude) if exclude else tuple()
    reqs = _get_requirements(path, exclude)
    return sca.process_requirements(PKG_MNGR, path, reqs, retry)
