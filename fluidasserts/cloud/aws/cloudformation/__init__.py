"""
Fluid Asserts AWS cloud package.

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# standard imports
from typing import Any, List, Dict, Callable, Set, Optional, Tuple
from collections import namedtuple
from contextvars import ContextVar
from contextlib import contextmanager
# 3d imports
import networkx as nx
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes
# local imports
from fluidasserts import Unit, OPEN, CLOSED
from fluidasserts.cloud.aws.cloudformation.loader import Dict \
    as ADict

# Containers
Vulnerability = namedtuple('Vulnerability', [
    'path',
    'entity',
    'identifier',
    'reason',
    'line'], defaults=[None, None, None, None, 0])

GRAPHS = ContextVar('Graphs', default=DiGraph())


def _index(dictionary: dict, indexes: List[Any], default: Any = None) -> Any:
    """Safely Index a dictionary over indexes without KeyError opportunity."""
    if len(indexes) < 2:
        raise AssertionError('indexes length must be >= two')
    result = dictionary.get(indexes[0], {})
    for index in indexes[1:-1]:
        result = result.get(index, {})
    result = result.get(indexes[-1], default)
    return result


def _get_result_as_tuple(*,
                         vulnerabilities: List[Vulnerability],
                         msg_open: str, msg_closed: str) -> tuple:
    """Return the tuple version of the Result object."""
    # Example:
    # - where: {path}
    #   specific: {entity}/{id} {reason}

    vuln_units: List[Unit] = [
        Unit(where=f'{x.path} - [{x.identifier}] {x.entity} {x.reason}.',
             specific=[x.line])
        for x in vulnerabilities]

    if vuln_units:
        return OPEN, msg_open, vuln_units
    return CLOSED, msg_closed, vuln_units


@contextmanager
def templates_as_graph(path: str, exclude: List[str] = None) -> DiGraph:
    """Yield a graph with all the templates inside the path."""
    _graph: DiGraph = DiGraph()
    ADict.load_templates(path, _graph, exclude)
    yield _graph


def get_ref_nodes(graph: DiGraph, node: int,
                  condition: Callable = None) -> List[int]:
    """
    Returns the value of a node the value of its reference.

    If the node already has a value, the same node is returned, otherwise the
    references that meet the condition are searched.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param condition: Condition that the reference value must meet,
        a boolean must return.
    """
    if not condition:
        def condition(  # noqa pylint: disable=function-redefined
            value): return True  # noqa pylint: disable=unused-argument,multiple-statements
    nodes: List[int] = [node] if 'value' in graph.nodes[node] else [
        ref for ref in dfs_preorder_nodes(graph, node, 3)
        if 'value' in graph.nodes[ref] and condition(graph.nodes[ref]['value'])
    ]
    return nx.utils.flatten(nodes)


def get_type(graph: DiGraph, node: int, allowed_types: Set[str]) -> str:
    """
    Returns the predecessor that are within the allowed types.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param allowed_types: Nodes that can be found within the predecessors.
    """
    _type = None
    intersec = graph.nodes[node]['labels'].intersection(allowed_types)
    if intersec:
        _type = list(intersec)[-1]
    else:
        for _ in range(5):
            node = list(graph.predecessors(node))
            node = node[0]
            intersec = graph.nodes[node]['labels'].intersection(allowed_types)
            if intersec:
                _type = list(intersec)[-1]
                break
    return _type


def get_predecessor(graph: DiGraph, node: int, label: str) -> int:
    """
    Returns the node of the first predecessor that contains the label.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param label: Nodes that can be found within the predecessors.
    """
    predecessor = None
    for _ in range(10):
        node = list(graph.predecessors(node))[0]
        if label in graph.nodes[node]['labels']:
            predecessor = node
            break
    return predecessor


def get_graph(path: str, exclude: Optional[List[str]] = None) -> DiGraph:
    """Returns a graph with all the templates inside the path"""
    _graph: DiGraph = GRAPHS.get()
    GRAPHS.set(ADict.load_templates(path=path, graph=_graph, exclude=exclude))
    return GRAPHS.get()


def get_templates(graph: DiGraph, exclude: Optional[List[str]] = None
                  ) -> List[Tuple[int, Dict]]:
    """Returns the templates that are inside a graph."""
    templates = [(_id, node) for _id, node in graph.nodes.data()
                 if 'CloudFormationTemplate' in node['labels']]
    if exclude:
        templates = filter(
            lambda _id, node: not any(ex in node['path'] for ex in exclude),
            templates)
    return templates
