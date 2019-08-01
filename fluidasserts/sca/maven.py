# -*- coding: utf-8 -*-

"""Software Composition Analysis for Maven packages."""

# standard imports
import os

# 3rd party imports
from pyparsing import Suppress, Keyword, MatchFirst, quotedString, Optional
from defusedxml.ElementTree import parse

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import sca
from fluidasserts.helper import asynchronous
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import track, level, notify

PKG_MNGR = 'maven'


def _get_requirements_pom_xml(path: str) -> list:
    """
    Get list of requirements from Maven project.

    Files supported are pom.xml

    :param path: Project path
    """
    reqs = []
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    for full_path in get_paths(path, endswith=('pom.xml',)):
        tree = parse(full_path)
        root = tree.getroot()
        deps = root.findall(".//xmlns:dependency",
                            namespaces=namespaces)
        for dep in deps:
            artifact_id = dep.find("xmlns:artifactId",
                                   namespaces=namespaces)
            version = dep.find("xmlns:version", namespaces=namespaces)
            if version is not None:
                if version.text.startswith('$'):
                    reqs.append((full_path, artifact_id.text, None))
                else:
                    reqs.append((full_path, artifact_id.text, version.text))
            else:
                reqs.append((full_path, artifact_id.text, None))
    return reqs


def _get_requirements_build_gradle(path: str) -> list:
    """
    Get list of requirements from Maven project.

    Files supported are build.gradle

    :param path: Project path
    """
    reqs = []
    for file_path in get_paths(path, endswith=('build.gradle',)):
        with open(file_path, encoding='latin-1') as file_fd:
            file_content = file_fd.read()

        string = MatchFirst([quotedString('"'), quotedString("'")])
        string.setParseAction(lambda x: [x[0][1:-1]])

        grammars: list = [
            Suppress(Keyword('compile') + Optional('(')) +
            string.copy()('package'),
            Suppress(Keyword('compile') + Optional('(')) +
            Suppress(Keyword('group') + ':') +
            string.copy()('group') + Suppress(',') +
            Suppress(Keyword('name') + ':') +
            string.copy()('name') + Suppress(',') +
            Suppress(Keyword('version') + ':') +
            string.copy()('version'),
        ]

        for grammar in grammars:
            for tokens, _, _ in grammar.scanString(file_content):
                matches = tokens.asDict()
                if 'package' in matches:
                    if ':' in matches['package']:
                        name, version = matches['package'].rsplit(':', 1)
                    else:
                        name, version = matches['package'], None
                    reqs.append((file_path, name, version))
                else:
                    reqs.append((file_path,
                                 f"{matches['group']}:{matches['name']}",
                                 matches['version']))
                    reqs.append(
                        (file_path, matches['group'], matches['version']))
    return reqs


def _get_requirements(path: str) -> list:
    """
    Return a list of requirements from a Maven project.

    Files supported are pom.xml and build.graddle.

    :param path: Project path
    """
    reqs = list()
    if not os.path.exists(path):
        return reqs
    return _get_requirements_pom_xml(path) + \
        _get_requirements_build_gradle(path)


def _parse_requirements(reqs: set) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    has_vulns, proj_vulns = None, {}
    results_ossindex = asynchronous.run_func(
        sca.get_vulns_ossindex_async,
        [((PKG_MNGR, path, dep, ver), {}) for path, dep, ver in reqs])
    results = filter(
        lambda x: isinstance(x, tuple), results_ossindex)
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
