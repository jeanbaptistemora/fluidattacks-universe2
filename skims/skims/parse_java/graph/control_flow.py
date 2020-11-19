"""Walk the graph and append edges with the possible code execution flow."""

# Third party libraries
import networkx as nx
from more_itertools import (
    windowed,
)


def _analyze_if_then_statement(graph: nx.OrderedDiGraph) -> None:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs.get('label_type') == 'IfThenStatement':
            # Find the ifThenStatement `then` node
            then_id = tuple(graph.adj[n_id])[4]
            graph.add_edge(
                n_id,
                then_id,
                label_cfg='CFG',
                label_true='True',
            )
        elif n_attrs.get('label_type') == 'IfThenElseStatement':
            # Find the ifThenStatement `then` and `else` node
            then_id = tuple(graph.adj[n_id])[4]
            else_id = tuple(graph.adj[n_id])[6]
            graph.add_edge(
                n_id,
                then_id,
                label_cfg='CFG',
                label_true='True',
            )
            graph.add_edge(
                n_id,
                else_id,
                label_cfg='CFG',
                label_false='False',
            )


def _analyze_block_statements(graph: nx.OrderedDiGraph) -> None:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs.get('label_type') == 'BlockStatement':
            for a_id, b_id in windowed(graph.adj[n_id], 2):
                graph.add_edge(
                    a_id,
                    b_id,
                    label_e='e',
                    label_cfg='CFG',
                )


def analyze(graph: nx.OrderedDiGraph) -> None:
    _analyze_if_then_statement(graph)
    _analyze_block_statements(graph)
