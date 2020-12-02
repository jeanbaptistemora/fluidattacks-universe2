"""Modify in-place sub-trees of the graph in order to simplify it."""

# Third party libraries
import networkx as nx


def _mark_methods(graph: nx.DiGraph) -> None:
    for n_attrs in graph.nodes.values():
        if n_attrs['label_type'] == 'MethodDeclaration':
            n_attrs['label_input_type'] = 'function'


def mark(graph: nx.DiGraph) -> None:
    _mark_methods(graph)
