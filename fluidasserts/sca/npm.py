# -*- coding: utf-8 -*-

"""Software Composition Analysis for NodeJS packages."""

# standard imports
import json
import os

# 3rd party imports
# None

# local imports
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import track, level, notify

PKG_MNGR = 'npm'


def _get_all_versions(json_obj: dict) -> None:
    """Return all dependencies and requirements in the given json_obj."""
    deps = []
    if isinstance(json_obj, dict):
        # In a package.json
        #    'dependencies': {
        #        '$dep': '$version'
        #        ...
        #    }

        # In a package-lock.json
        #    'dependencies': {
        #        '$dep': {
        #            'version': '$version',
        #            'requires': {
        #                 'req': '$version'
        #                 ...
        #                 ...it may be nested from this point on
        #            }
        #        }
        #        ...
        #    }

        for dep, metadata in json_obj.get('dependencies', {}).items():
            if isinstance(metadata, str):
                deps.append((dep, metadata))
            elif isinstance(metadata, dict):
                if 'version' in metadata:
                    deps.append((dep, metadata['version']))
                if 'requires' in metadata and \
                        isinstance(metadata['requires'], dict):
                    for req, version in metadata['requires'].items():
                        deps.append((req, version))
                deps.extend(_get_all_versions(metadata))
    return deps


def _get_requirements(path: str, exclude: tuple) -> set:
    """
    Get a list of requirements from NPM project.

    Files supported are package.json and package-lock.json

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = set()
    if not os.path.exists(path):
        return reqs
    endswith = ('package.json', 'package-lock.json')
    dictionary = {ord(c): None for c in '^~<=>'}
    for path in get_paths(path, endswith=endswith, exclude=exclude):
        with open(path) as file:
            data = json.load(file)
        reqs.update(
            (path, dep, ver.translate(dictionary))
            for dep, ver in _get_all_versions(data))
    return reqs


@notify
@level('high')
@track
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    return sca.process_requirement(PKG_MNGR, package, version, retry)


@notify
@level('high')
@track
def project_has_vulnerabilities(
        path: str, exclude: list = None, retry: bool = True) -> bool:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    exclude = tuple(exclude) if exclude else tuple()
    reqs = _get_requirements(path, exclude)
    return sca.process_requirements(PKG_MNGR, path, reqs, retry)
