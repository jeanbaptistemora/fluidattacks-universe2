# -*- coding: utf-8 -*-

"""Software Composition Analysis for Maven packages."""

# standard imports
import os

# 3rd party imports
from pyparsing import Suppress, Keyword, MatchFirst, quotedString, Optional
from defusedxml.ElementTree import parse

# local imports
from fluidasserts import HIGH, SAST
from fluidasserts.helper import sca
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import api

PKG_MNGR = 'maven'


def _get_requirements_pom_xml(path: str, exclude: tuple) -> list:
    """
    Get list of requirements from Maven project.

    Files supported are pom.xml

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = []
    endswith = ('pom.xml',)
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    for full_path in get_paths(path, endswith=endswith, exclude=exclude):
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


def _get_requirements_build_gradle(path: str, exclude: tuple) -> list:
    """
    Get list of requirements from Maven project.

    Files supported are build.gradle

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = []
    endswith = ('build.gradle',)
    for file_path in get_paths(path, endswith=endswith, exclude=exclude):
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
                    # The convention is Group:Name:Version
                    if matches['package'].count(':') >= 2:
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


def _get_requirements(path: str, exclude: tuple) -> list:
    """
    Return a list of requirements from a Maven project.

    Files supported are pom.xml and build.graddle.

    :param path: Project path
    :param exclude: Paths that contains any string from this tuple are ignored.
    """
    reqs = list()
    if not os.path.exists(path):
        return reqs
    return _get_requirements_pom_xml(path, exclude) + \
        _get_requirements_build_gradle(path, exclude)


@api(risk=HIGH, kind=SAST)
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> tuple:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    :rtype: :class:`fluidasserts.Result`
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)


@api(risk=HIGH, kind=SAST)
def project_has_vulnerabilities(
        path: str, exclude: list = None, retry: bool = True) -> tuple:
    """
    Search vulnerabilities on given project directory.

    :param path: Project path.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    exclude = tuple(exclude) if exclude else tuple()
    reqs = _get_requirements(path, exclude)
    return sca.process_requirements(PKG_MNGR, path, reqs, retry)
