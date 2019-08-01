# -*- coding: utf-8 -*-

"""Software Composition Analysis for NodeJS packages."""

# standard imports
import json
import os

# 3rd party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import sca
from fluidasserts.helper import asynchronous
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


def _get_requirements(path: str) -> set:
    """
    Get a list of requirements from NPM project.

    Files supported are package.json and package-lock.json

    :param path: Project path
    """
    reqs = set()
    if not os.path.exists(path):
        return reqs
    dictionary = {ord(c): None for c in '^~<=>'}
    for path in get_paths(path, endswith=(
            'package.json', 'package-lock.json')):
        with open(path) as file:
            data = json.load(file)
        reqs.update(
            (path, dep, ver.translate(dictionary))
            for dep, ver in _get_all_versions(data))
    return reqs


def _parse_requirements(reqs: set) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    has_vulns, proj_vulns = None, {}
    results = asynchronous.run_func(
        sca.get_vulns_ossindex_async,
        [((PKG_MNGR, path, dep, ver), {}) for path, dep, ver in reqs])
    results = filter(lambda x: isinstance(x, tuple), results)
    for path, dep, ver, vulns in results:
        if vulns:
            has_vulns = True
            try:
                proj_vulns[path][f'{dep} {ver}'] = vulns
            except KeyError:
                proj_vulns[path] = {f'{dep} {ver}': vulns}
    return has_vulns, proj_vulns


@notify
@level('high')
@track
def package_has_vulnerabilities(package: str, version: str = None) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    return sca.get_vulns_from_ossindex(PKG_MNGR, package, version)


@notify
@level('high')
@track
def project_has_vulnerabilities(path: str) -> bool:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    """
    reqs = _get_requirements(path)
    if not reqs:
        show_unknown('Not packages found in project',
                     details=dict(path=path))
        return False
    has_vulns, proj_vulns = _parse_requirements(reqs)
    if has_vulns:
        show_open('Project has dependencies with vulnerabilities',
                  details=dict(project_path=path,
                               vulnerabilities=proj_vulns))
        return True
    show_close('Project has not dependencies with vulnerabilities',
               details=dict(project_path=path))
    return False
