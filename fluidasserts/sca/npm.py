# -*- coding: utf-8 -*-
"""Software Composition Analysis for NodeJS packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts import HIGH, SCA
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import api
from fluidasserts.utils.parsers import json as l_json
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts.helper import asynchronous
from fluidasserts import Unit
from fluidasserts.utils.generic import get_sha256

PKG_MNGR = 'npm'


def _get_all_versions(json_obj: dict) -> None:
    """Return all dependencies and requirements in the given json_obj."""
    deps = []
    if isinstance(json_obj, (dict, l_json.CustomDict)):
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
                deps.append((dep, metadata,
                             json_obj['dependencies'][f'{dep}.line']))
            elif isinstance(metadata, (dict, l_json.CustomDict)):
                if 'version' in metadata:
                    deps.append((dep, metadata['version'],
                                 json_obj['dependencies'][f'{dep}.line']))
                if 'requires' in metadata and isinstance(
                        metadata['requires'], (dict, l_json.CustomDict)):
                    for req, version in metadata['requires'].items():
                        deps.append((req, version,
                                     metadata['requires'][f'{req}.line']))
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
    for fpath in get_paths(path, endswith=endswith, exclude=exclude):
        with open(fpath) as file:
            data = l_json.parse(file.read())
        reqs.update((fpath, dep, ver.translate(dictionary), line)
                    for dep, ver, line, in _get_all_versions(data))
    return reqs


def _get_vuln_line(reqs: list, pkg: str, ver: str) -> int:
    """Return the line of first occurrence of pkg and version in path or 0."""
    line = list(
        map(lambda y: y[3], filter(lambda x: x[1] == pkg and x[2] == ver,
                                   reqs)))
    return line[0] if line else 0


def _process_requirements(path: str,
                          reqs: set,
                          vulnerable_dependencies: dict = None,
                          retry: bool = True) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    vulnerable_dependencies = vulnerable_dependencies or {}
    if path and not os.path.exists(path):
        return UNKNOWN, 'File does not exist'
    if not reqs:
        return CLOSED, 'No packages have been found in that path'

    results = asynchronous.run_func(sca.get_vulns_vulndb_async,
                                    [(('npm', _path, dep, ver), {
                                        'retry': retry
                                    }) for _path, dep, ver, _ in reqs])
    results = list(filter(lambda x: isinstance(x, tuple), results))

    has_vulns, proj_vulns = None, {}
    for _path, dep, ver, vulns in results:
        in_custom_vulns = ver in vulnerable_dependencies.get(dep, [])
        if vulns or in_custom_vulns:
            has_vulns = True
            component = (dep, ver)
            try:
                proj_vulns[_path].update({component: vulns})
            except KeyError:
                proj_vulns[_path] = {component: vulns}

    vulns = [
        Unit(
            where=f'{_path} [{pkg}@{ver if ver else "unpinned"}]',
            source='Lines',
            specific=[_get_vuln_line(reqs, pkg, ver)],
            fingerprint={
                'sha256': get_sha256(_path),
                'vulnerabilities': deps[(pkg, ver)],
            }) for _path, deps in proj_vulns.items() for pkg, ver in deps
    ]

    if has_vulns:
        return OPEN, 'Project has dependencies with vulnerabilities', vulns
    return CLOSED, 'Project has dependencies with vulnerabilities'


@api(risk=HIGH, kind=SCA)
def package_has_vulnerabilities(package: str,
                                version: str = None,
                                retry: bool = True) -> tuple:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    :rtype: :class:`fluidasserts.Result`
    """
    reqs = set([(None, package, version, 0)])
    return _process_requirements(None, reqs, retry=retry)


@api(risk=HIGH, kind=SCA)
def project_has_vulnerabilities(path: str,
                                exclude: list = None,
                                vulnerable_dependencies: dict = None,
                                retry: bool = True) -> tuple:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    exclude = tuple(exclude) if exclude else tuple()
    reqs = _get_requirements(path, exclude)
    return _process_requirements(
        path,
        reqs,
        vulnerable_dependencies=vulnerable_dependencies,
        retry=retry)
