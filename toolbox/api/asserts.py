#! /usr/bin/env python3

# Standard library
import os
from typing import (
    Any,
    Dict,
    Iterator,
    NamedTuple,
    Tuple
)
from itertools import repeat

# Third parties libraries
import ruamel.yaml as yaml

# Constants
NODE = Dict[str, Any]


class Error(Exception):
    """Base class for all errors in this module."""


class ExploitError(Error):
    """Exploit have ERROR nodes in its output."""


Vulnerability = NamedTuple('Vulnerability', [
    # Context properties
    ('finding_title', str),
    ('finding_id', str),

    # Asserts properties
    ('status', str),
    ('what', str),
    ('where', str),
    ('kind', str),
])


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
    return _is_node_a_result(node) and node['status'].startswith('ERROR')


def _is_node_an_unknown_result(node: NODE) -> bool:
    """True if the node is an UNKNOWN result node."""
    return _is_node_a_result(node) and node['status'] == 'UNKNOWN'


def _is_node_a_sast_result(node: NODE) -> bool:
    """True if the node is a SAST result node."""
    return _is_node_a_result(node) and _get_node_kind(node) == 'SAST'


def _is_node_a_sca_result(node: NODE) -> bool:
    """True if the node is a SCA result node."""
    return _is_node_a_result(node) and _get_node_kind(node) == 'SCA'


def _is_node_a_dast_result(node: NODE) -> bool:
    """True if the node is a DAST result node."""
    return _is_node_a_result(node) and _get_node_kind(node) == 'DAST'


def _is_node_a_iast_result(node: NODE) -> bool:
    """True if the node is a Generic result node."""
    return _is_node_a_result(node) \
        and _get_node_kind(node) in ('IAST', 'Generic')


def _is_node_an_iexp_result(node: NODE) -> bool:
    """True if node contains parameter.metadata keys."""
    return 'parameters' in node \
        and 'metadata' in node['parameters'] \
        and node['parameters']['metadata']


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


def _get_node_result_status(node: NODE) -> str:
    """Return the status of a result node."""
    return node['status']


def _get_node_repo(node: NODE) -> str:
    """Return the repository from a repository node."""
    return node['repository']


def _get_node_finding(node: NODE) -> str:
    """Return the finding from a finding node."""
    return node['finding']


def _get_node_kind(node: NODE) -> str:
    return node.get('test_kind', '')


def _get_node_sast_results(node: NODE, current_repo: str
                           ) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Path, Where) for the given node vulnerabilities."""
    for vulnerability in node.get('vulnerabilities', []):
        where: str = vulnerability['where']
        specific: str = vulnerability.get('specific', '0')
        full_where: str = os.path.normpath(os.path.join(current_repo, where))
        yield from zip(repeat('SAST'),
                       repeat(full_where),
                       _helper_split_specific(specific))


def _get_node_sca_results(node: NODE, current_repo: str
                          ) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, Path, Where) for the given node vulnerabilities."""
    for vulnerability in node.get('vulnerabilities', []):
        where: str = vulnerability['where']
        specific: str = vulnerability.get('specific', '0')
        full_where: str = os.path.normpath(os.path.join(current_repo, where))
        yield from zip(repeat('SCA'),
                       repeat(full_where),
                       _helper_split_specific(specific))


def _get_node_dast_results(node: NODE) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, What, Where) for the given node vulnerabilities."""
    for vulnerability in node.get('vulnerabilities', []):
        what: str = vulnerability['where']
        yield from zip(repeat('DAST'),
                       repeat(what),
                       _helper_split_specific(
                           vulnerability.get('specific', '')))


def _get_node_iast_results(node: NODE) -> Iterator[Tuple[str, str, str]]:
    """Yield (Kind, What, Where) for the given node vulnerabilities."""
    if _is_node_an_iexp_result(node):
        metadata = node['parameters']['metadata']
        description = metadata.get('description', '')
        attack_vector = metadata.get('attack_vector', '')
        yield ('IAST', description, attack_vector)
    else:
        for vulnerability in node.get('vulnerabilities', []):
            what: str = vulnerability['where']
            yield from zip(
                repeat('IAST'),
                repeat(what),
                _helper_split_specific(
                    vulnerability.get('specific', '')))


def iterate_open_results_from_content(
        asserts_output: str,
        default_repo: str = '.') -> Iterator[Tuple[str, str, str]]:
    for vulnerability in \
            iterate_vulnerabilities_from_content(asserts_output, default_repo):
        if vulnerability.status == 'OPEN':
            yield (
                vulnerability.kind,
                vulnerability.what,
                vulnerability.where,
            )


def iterate_vulnerabilities_from_content(
        asserts_output: str,
        default_repo: str = '.',
) -> Iterator[Vulnerability]:
    """Yield vulnerabilities and its attributes from the asserts_output."""
    bare_nodes: Tuple[NODE, ...] = tuple(yaml.safe_load_all(asserts_output))
    relevant_nodes: Tuple[NODE, ...] = tuple(filter(_is_relevant, bare_nodes))

    current_finding_id: str = ''
    current_finding_title: str = 'unknown-finding'
    current_repo: str = default_repo
    current_result_status: str
    for node in relevant_nodes:
        if _is_node_a_repo_marker(node):
            current_repo = _get_node_repo(node)
        elif _is_node_a_finding_marker(node):
            current_finding_title = _get_node_finding(node)
        elif _is_node_a_result(node):
            current_result_status = _get_node_result_status(node)
            vulnerability_iterators = {
                _is_node_a_dast_result(node):
                _get_node_dast_results(node),
                _is_node_a_sast_result(node):
                _get_node_sast_results(node, current_repo),
                _is_node_a_sca_result(node):
                _get_node_sca_results(node, current_repo),
                _is_node_a_iast_result(node):
                _get_node_iast_results(node),
            }

            for kind, what, where in vulnerability_iterators.get(True, []):
                yield Vulnerability(
                    finding_id=current_finding_id,
                    finding_title=current_finding_title,
                    status=current_result_status,
                    kind=kind,
                    what=what,
                    where=where,
                )

            # Some node types like unknown or error do not have whats
            #   and wheres associated to them
            # Let's yield a default vulnerability just to symbolize they exist
            if 'vulnerabilities' not in node:
                yield Vulnerability(
                    finding_id=current_finding_id,
                    finding_title=current_finding_title,
                    status=current_result_status,
                    kind='',
                    what='',
                    where='',
                )


def iterate_open_results_from_file(
        asserts_output_path: str,
        default_repo: str = '.') -> Iterator[Tuple[str, str, str]]:
    """Yield (kind, what, where) tuples of open checks in the exploit."""
    with open(asserts_output_path, 'r') as handle:
        yield from \
            iterate_open_results_from_content(handle.read(), default_repo)


def iterate_vulnerabilities_from_file(
    asserts_output_path: str,
    default_repo: str = '.',
) -> Iterator[Vulnerability]:
    """Yield (kind, what, where, status) of open checks in the exploit."""
    with open(asserts_output_path, 'r') as handle:
        yield from \
            iterate_vulnerabilities_from_content(handle.read(), default_repo)


def get_exp_result_summary(asserts_output: str):
    """Return the summary of a exploit result."""
    asserts_result = tuple(yaml.safe_load_all(asserts_output))
    if not asserts_result:
        return {}

    return asserts_result[-1].get('summary', {})


def get_exp_error_message(asserts_output: str) -> str:
    """Return one of the error messages from a exploit, or null str."""
    bare_nodes: Tuple[NODE, ...] = tuple(yaml.safe_load_all(asserts_output))
    relevant_nodes: Tuple[NODE, ...] = tuple(filter(_is_relevant, bare_nodes))

    error_nodes = tuple(filter(_is_node_an_error_result, relevant_nodes))
    if error_nodes:
        return error_nodes[0]['status']

    return str()
