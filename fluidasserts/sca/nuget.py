# -*- coding: utf-8 -*-

"""Software Composition Analysis for NuGet (C#) packages."""

# standard imports
import os

# 3rd party imports
from defusedxml.ElementTree import parse

# local imports
from fluidasserts import Result
from fluidasserts import HIGH
from fluidasserts import SAST
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import api

PKG_MNGR = 'nuget'


def _get_requirements(path: str, exclude: tuple) -> set:
    """
    Get list of requirements from NuGet project.

    Files supported are packages.config

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = set()
    if not os.path.exists(path):
        return reqs
    endswith = ('packages.config',)
    for full_path in get_paths(path, endswith=endswith, exclude=exclude):
        reqs.update(
            (path, dep.attrib['id'], dep.attrib['version'])
            for dep in parse(full_path).findall(".//package"))
    return reqs


@api(risk=HIGH, kind=SAST)
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> Result:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)


@api(risk=HIGH, kind=SAST)
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
