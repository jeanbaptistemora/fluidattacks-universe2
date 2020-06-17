# -*- coding: utf-8 -*-
"""Fluid Asserts AWS cloudformation graphs package."""

# standar imports
from contextlib import contextmanager
from typing import Callable
from typing import List
from typing import Set

# 3rd party imports
import networkx as nx
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes

# local imports
from fluidasserts.cloud.aws.cloudformation.graphs.new_loader import Dict \
    as ADict


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
    for _ in range(5):
        node = list(graph.predecessors(node))[0]
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
