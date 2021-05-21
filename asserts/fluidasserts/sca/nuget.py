# -*- coding: utf-8 -*-

"""Software Composition Analysis for NuGet (C#) packages."""

# standard imports
import os

# 3rd party imports
import defusedxml.ElementTree

# local imports
from fluidasserts import HIGH, SCA
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import api

PKG_MNGR = "nuget"


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
    endswith = ("packages.config",)
    for full_path in get_paths(path, endswith=endswith, exclude=exclude):
        parsed = defusedxml.ElementTree.parse(full_path)
        reqs.update(
            (full_path, dep.attrib["id"], dep.attrib["version"])
            for dep in parsed.findall(".//package")
        )
    return reqs


@api(risk=HIGH, kind=SCA)
def package_has_vulnerabilities(
    package: str, version: str = None, retry: bool = True
) -> tuple:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    :rtype: :class:`fluidasserts.Result`
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)


@api(risk=HIGH, kind=SCA)
def project_has_vulnerabilities(
    path: str, exclude: list = None, retry: bool = True
) -> tuple:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    exclude = tuple(exclude) if exclude else tuple()
    reqs = _get_requirements(path, exclude)
    return sca.process_requirements(PKG_MNGR, path, reqs, retry)
