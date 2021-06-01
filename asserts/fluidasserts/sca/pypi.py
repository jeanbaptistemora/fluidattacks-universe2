# -*- coding: utf-8 -*-

"""Software Composition Analysis for Python packages."""


import contextlib
from fluidasserts import (
    HIGH,
    SCA,
)
from fluidasserts.helper import (
    sca,
)
from fluidasserts.utils.decorators import (
    api,
)
from fluidasserts.utils.generic import (
    get_dir_paths,
)
import os
from requirements_detector import (
    find_requirements,
)
from requirements_detector.detect import (
    RequirementsNotFound,
)

PKG_MNGR = "pypi"


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
        with contextlib.suppress(RequirementsNotFound):
            reqs.update(
                (
                    req.location_defined,
                    req.name,
                    req.version_specs[0][1] if req.version_specs else None,
                )
                for req in find_requirements(full_path)
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
