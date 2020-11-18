"""Modify in-place sub-trees of the graph in order to simplify it."""

# Standard library
from typing import (
    List,
    Tuple,
)

# Third party libraries
import networkx as nx


def _chop_aux_nodes(graph: nx.OrderedDiGraph) -> None:
    nodes_to_chop: List[Tuple[str, str, str]] = []

    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] is None:
            # Structure: p -> n -> c
            p_id = n_attrs['label_parent_ast']
            c_id = tuple(graph.adj[n_id])[0]
            nodes_to_chop.append((p_id, n_id, c_id))

    for p_id, n_id, c_id in nodes_to_chop:
        # Before: p -> n -> c
        # After: p -> c
        graph.nodes[c_id]['label_parent_ast'] = p_id
        graph.add_edge(p_id, c_id, **graph[p_id][n_id])
        graph.remove_node(n_id)


def reduce(graph: nx.OrderedDiGraph) -> None:
    _chop_aux_nodes(graph)
