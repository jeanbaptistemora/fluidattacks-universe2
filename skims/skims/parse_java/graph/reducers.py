"""Modify in-place sub-trees of the graph in order to simplify it."""

# Standard library
from typing import (
    List,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def _patch_node_types(graph: nx.OrderedDiGraph) -> None:
    for n_attrs in graph.nodes.values():
        label_type: str = n_attrs['label_type']

        try:
            # Input format is regularly Name|index
            label_type, label_type_index = label_type.rsplit('|', maxsplit=1)

            n_attrs['label_type'] = label_type
            n_attrs['label_type_index'] = label_type_index
        except ValueError:
            # Some literal nodes have not the index
            n_attrs['label_type'] = label_type
            n_attrs['label_type_index'] = '0'


def _concatenate_child_texts(
    graph: nx.OrderedDiGraph,
    parent_label_type: str,
    childs_label_types: Tuple[str, ...],
) -> None:
    nodes_to_process = g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type=parent_label_type,
    ))

    nodes_to_edit: List[str] = [
        n_id
        for n_id in nodes_to_process
        for c_ids in [g.adj(graph, n_id)]
        if len(c_ids) == len(childs_label_types)
        and all(
            graph.nodes[c_id]['label_type'] == child_label_type
            for c_id, child_label_type in zip(c_ids, childs_label_types)
        )
    ]

    for n_id in nodes_to_edit:
        c_ids = g.adj(graph, n_id)
        n_attrs = graph.nodes[n_id]
        n_attrs['label_type'] = f'Custom{parent_label_type}'
        n_attrs['label_text'] = ''.join(
            graph.nodes[c_id]['label_text'] for c_id in c_ids
        )
        graph.remove_nodes_from(c_ids)


def _replace_with_child(
    graph: nx.OrderedDiGraph,
    parent_label_type: str,
    childs_label_type: str,
) -> None:
    nodes_to_process = g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type=parent_label_type,
    ))

    nodes_to_edit: List[Tuple[str, str]] = [
        (n_id, c_id)
        for n_id in nodes_to_process
        for c_id in g.adj(graph, n_id)
        if graph.nodes[c_id]['label_type'] == childs_label_type
    ]

    for n_id, c_id in reversed(nodes_to_edit):
        p_id = graph.nodes[n_id]['label_parent_ast']
        graph.nodes[c_id]['label_parent_ast'] = p_id
        graph.add_edge(p_id, c_id, **graph[p_id][n_id])
        graph.remove_node(n_id)


def reduce(graph: nx.OrderedDiGraph) -> None:
    _patch_node_types(graph)
    _concatenate_child_texts(graph, 'ClassType_lf_classOrInterfaceType', (
        'DOT',
        'IdentifierRule',
    ))
    _concatenate_child_texts(graph, 'ClassOrInterfaceType', (
        'IdentifierRule',
        'CustomClassType_lf_classOrInterfaceType',
    ))
    _concatenate_child_texts(graph, 'ClassType', (
        'CustomClassOrInterfaceType',
        'DOT',
        'IdentifierRule',
    ))
    _replace_with_child(graph, 'ExceptionTypeList', 'ExceptionType')
