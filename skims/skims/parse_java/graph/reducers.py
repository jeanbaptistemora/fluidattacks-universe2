"""Modify in-place sub-trees of the graph in order to simplify it."""

# Standard library
from typing import (
    List,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def _class_type_lf_class_or_interface_type(graph: nx.OrderedDiGraph) -> None:
    nodes_to_process = g.filter_nodes(
        graph,
        graph.nodes,
        g.pred_has_labels(label_type='ClassType_lf_classOrInterfaceType'),
    )

    nodes_to_edit: List[str] = [
        n_id
        for n_id in nodes_to_process
        for c_ids in [tuple(graph.adj[n_id])]
        if len(c_ids) == 2
        and graph.nodes[c_ids[0]]['label_type'] == 'DOT'
        and graph.nodes[c_ids[1]]['label_type'] == 'IdentifierRule'
    ]

    for n_id in nodes_to_edit:
        c_ids = tuple(graph.adj[n_id])
        graph.nodes[n_id]['label_type'] = 'CustomText'
        graph.nodes[n_id]['label_text'] = (
            graph.nodes[c_ids[0]]['label_text'] +
            graph.nodes[c_ids[1]]['label_text']
        )
        graph.remove_nodes_from(c_ids)


def reduce(graph: nx.OrderedDiGraph) -> None:
    _class_type_lf_class_or_interface_type(graph)
