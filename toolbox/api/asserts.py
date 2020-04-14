#! /usr/bin/env python3

# Standard library
import os
from typing import Any, Dict, Iterator, Tuple
from itertools import repeat

# Third parties libraries
import ruamel.yaml as yaml

# Local imports
from toolbox import logger

# Constants
NODE = Dict[str, Any]


class Error(Exception):
    """Base class for all errors in this module."""


class ExploitError(Error):
    """Exploit have ERROR nodes in its output."""


def _is_node_a_repo_marker(node: NODE) -> bool:
    """True if node contains the current repository name."""
    return any(x in node for x in ('repository',))


def _is_node_a_finding_marker(node: NODE) -> bool:
    """True if node contains the current repository name."""
    return any(x in node for x in ('finding',))


def _is_node_a_marker(node: NODE) -> bool:
    """True if node marks the starting of a testing section."""
    return any(f(node) for f in (_is_node_a_repo_marker,
                                 _is_node_a_finding_marker))


def _is_node_a_result(node: NODE) -> bool:
    """True if node is a check result node."""
    return all(x in node for x in ('status',))


def _is_node_an_open_result(node: NODE) -> bool:
    """True if the node is an OPEN result node."""
    return _is_node_a_result(node) and node['status'] == 'OPEN'


def _is_node_an_error_result(node: NODE) -> bool:
    """True if the node is an ERROR result node."""
    return _is_node_a_result(node) and node['status'] == 'ERROR'


def _is_node_a_sast_result(node: NODE) -> bool:
    """True if the node is a SAST result node."""
    return _is_node_a_result(node) and node['test_kind'] == 'SAST'


def _is_node_a_sca_result(node: NODE) -> bool:
    """True if the node is a SCA result node."""
    return _is_node_a_result(node) and node['test_kind'] == 'SCA'


def _is_node_a_dast_result(node: NODE) -> bool:
    """True if the node is a DAST result node."""
    return _is_node_a_result(node) and node['test_kind'] == 'DAST'


def _is_node_a_iast_result(node: NODE) -> bool:
    """True if the node is a Generic result node."""
    return _is_node_a_result(node) and node['test_kind'] in ('IAST', 'Generic')


def _is_node_a_mock_result(node: NODE) -> bool:
    """True if node contains parameter.metadata keys."""
    return 'parameters' in node \
        and 'metadata' in node['parameters']


def _is_relevant(node: NODE) -> bool:
    """True if the node is relevant for the checks that we are to perform."""
    return any(f(node) for f in (_is_node_a_marker, _is_node_a_result))


def _helper_split_specific(specific: str) -> Iterator[str]:
    """Split the escaped csv retrieved by Asserts."""
    # Asserts algorithm:
    #  - per every input in a list of inputs
    #    - replace '\' by '\\'
    #    - replace ',' by '\,'
    #  - join the list of inputs with ','
    #
    # Below is the inverse algorithm:
    item: str = str()
    escaping: bool = False
    for char in specific:
        if escaping:
            if char in ('\\', ','):
                item += char
                escaping = False
            else:
                raise Error('Found escaped char that does not need escaping')
        else:
            if char == '\\':
                escaping = True
            elif char == ',':
                yield item.strip()
                item = str()
            else:
                item += char
    yield item.strip()


def _get_node_repo(node: NODE) -> str:
    """Return the repository from a repository node."""
    return node['repository']


def _get_node_finding(node: NODE) -> str:
    """Return the finding from a finding node."""
    return node['finding']


def _get_node_sast_results(node: NODE, current_repo: str
                           ) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Path, Where) for the given node vulnerabilities."""
    for vulnerability in node['vulnerabilities']:
        where: str = vulnerability['where']
        specific: str = vulnerability.get('specific', '0')
        full_where: str = os.path.normpath(os.path.join(current_repo, where))
        yield from zip(repeat('SAST'),
                       repeat(full_where),
                       _helper_split_specific(specific))


def _get_node_sca_results(node: NODE, current_repo: str
                          ) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Path, Where) for the given node vulnerabilities."""
    for vulnerability in node['vulnerabilities']:
        where: str = vulnerability['where']
        specific: str = vulnerability.get('specific', '0')
        full_where: str = os.path.normpath(os.path.join(current_repo, where))
        yield from zip(repeat('SCA'),
                       repeat(full_where),
                       _helper_split_specific(specific))


def _get_node_dast_results(node: NODE) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Who, Where) for the given node vulnerabilities."""
    for vulnerability in node['vulnerabilities']:
        who: str = vulnerability['where']
        yield from zip(repeat('DAST'),
                       repeat(who),
                       _helper_split_specific(
                           vulnerability.get('specific', '')))


def _get_node_iast_results(node: NODE) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Who, Where) for the given node vulnerabilities."""
    if _is_node_a_mock_result(node):
        # A mock
        metadata = node['parameters']['metadata']
        description = metadata.get('description', '')
        attack_vector = metadata.get('attack_vector', '')
        yield ('IAST', description, attack_vector)
    else:
        for vulnerability in node['vulnerabilities']:
            who: str = vulnerability['where']
            yield from zip(
                repeat('IAST'),
                repeat(who),
                _helper_split_specific(
                    vulnerability.get('specific', '')))


def iterate_results_from_content(
        asserts_output: str,
        default_repo: str = '.') -> Iterator[Tuple[str, str, str]]:
    bare_nodes: Tuple[NODE, ...] = tuple(yaml.safe_load_all(asserts_output))
    relevant_nodes: Tuple[NODE, ...] = tuple(filter(_is_relevant, bare_nodes))

    # Quality Assertions
    if any(map(_is_node_an_error_result, relevant_nodes)):
        logger.warn(f'Some parts of the exploit contain errors!')

    current_repo: str = default_repo
    for node in relevant_nodes:
        if _is_node_a_repo_marker(node):
            current_repo = _get_node_repo(node)
        elif _is_node_a_finding_marker(node):
            _get_node_finding(node)
        elif _is_node_an_open_result(node):
            if _is_node_a_dast_result(node):
                yield from _get_node_dast_results(node)
            elif _is_node_a_sast_result(node):
                yield from _get_node_sast_results(node, current_repo)
            elif _is_node_a_sca_result(node):
                yield from _get_node_sca_results(node, current_repo)
            elif _is_node_a_iast_result(node):
                yield from _get_node_iast_results(node)


def iterate_results_from_file(
        asserts_output_path: str,
        default_repo: str = '.') -> Iterator[Tuple[str, str, str]]:
    """Yield (kind, who, where) tuples of open checks in the exploit."""
    with open(asserts_output_path, 'r') as handle:
        yield from iterate_results_from_content(handle.read(), default_repo)


def get_exp_result_summary(asserts_output_path: str):
    """Return the summary of a exploit result."""
    if not os.path.exists(asserts_output_path):
        return {}

    with open(asserts_output_path, 'r') as handle:
        asserts_result = tuple(yaml.safe_load_all(handle.read()))

        return asserts_result[-1].get('summary', {})
