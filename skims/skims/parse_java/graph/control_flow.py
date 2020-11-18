"""Walk the graph and append edges with the possible code execution flow."""

# Standar libraries
from typing import (
    Any,
    Tuple,
)
from contextlib import (
    suppress,
)

# Third party libraries
import networkx as nx

# Local import
from utils.graph import (
    has_label,
)


def _get_successors_by_label(
    graph: nx.OrderedDiGraph,
    source: Any,
    *labels: Any,
    depth_limit: int = 1,
) -> Tuple[Any, ...]:
    return tuple(successor for _, successors in nx.dfs_successors(
        graph,
        source=source,
        depth_limit=depth_limit,
    ).items() for successor in successors if has_label(
        graph.nodes[successor],
        *labels,
    ))


def _analyze_if_then_statement(graph: nx.OrderedDiGraph) -> None:
    for node_id, node in graph.nodes.items():
        if has_label(node, 'IfThenStatement'):
            # an ifThenStatement should only have one Statement
            true_statement = _get_successors_by_label(
                graph,
                node_id,
                'Statement',
                depth_limit=1,
            )[0]
            graph.add_edge(
                node_id,
                true_statement,
                label_cfg='CFG',
                label_true='True',
            )
        elif has_label(node, 'IfThenElseStatement'):
            true_statement = _get_successors_by_label(
                graph,
                node_id,
                'StatementNoShortIf',
                depth_limit=1,
            )[0]
            graph.add_edge(
                node_id,
                true_statement,
                label_cfg='CFG',
                label_true='True',
            )
            false_statement = _get_successors_by_label(
                graph,
                node_id,
                'Statement',
                depth_limit=1,
            )[0]
            graph.add_edge(
                node_id,
                false_statement,
                label_cfg='CFG',
                label_false='False',
            )


def _analyze_block_statements(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    for node_id, node in graph.nodes.items():
        if has_label(node, 'BlockStatement'):
            statements = nx.dfs_successors(
                graph,
                source=node_id,
                depth_limit=2,
            )[node_id]
            for index, statement in enumerate(statements):
                with suppress(IndexError):
                    graph.add_edge(
                        statement,
                        statements[index + 1],
                        label_type='e',
                        label_cfg='CFG',
                    )
    return graph


def analyze(graph: nx.OrderedDiGraph) -> None:
    _analyze_if_then_statement(graph)
    _analyze_block_statements(graph)
