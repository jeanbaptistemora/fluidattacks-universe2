"""Walk the graph and append edges with the possible code execution flow."""
# Standar libraries
from typing import (
    Any,
    Tuple,
)

# Third party libraries
import networkx as nx
from more_itertools import (
    windowed,
)
from utils.graph import (
    has_labels,
)


def _get_successors_by_label(
    graph: nx.OrderedDiGraph,
    source: Any,
    depth_limit: int = 1,
    **labels: Any,
) -> Tuple[Any, ...]:
    return tuple(successor for _, successors in nx.dfs_successors(
        graph,
        source=source,
        depth_limit=depth_limit,
    ).items() for successor in successors if has_labels(
        graph.nodes[successor],
        **labels,
    ))


def _analyze_if_then_statement(graph: nx.OrderedDiGraph) -> None:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs.get('label_type') == 'IfThenStatement':
            # Find the ifThenStatement `then` node
            then_id = tuple(graph.adj[n_id])[4]
            graph.add_edge(
                n_id,
                then_id,
                label_cfg='CFG',
                label_true='true',
            )
        elif n_attrs.get('label_type') == 'IfThenElseStatement':
            # Find the ifThenStatement `then` and `else` node
            then_id = tuple(graph.adj[n_id])[5]
            else_id = tuple(graph.adj[n_id])[6]
            graph.add_edge(
                n_id,
                then_id,
                label_cfg='CFG',
                label_true='true',
            )
            graph.add_edge(
                n_id,
                else_id,
                label_cfg='CFG',
                label_false='false',
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


def _analyze_while_statements(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs.get('label_type') not in ('WhileStatement', 'DoStatement'):
            continue
        else_id = tuple(graph.adj[n_id])[-1]
        while_block_statement = _get_successors_by_label(
            graph,
            n_id,
            depth_limit=2,
            label_type='BlockStatement',
        )[0]
        statements = tuple(graph.adj[while_block_statement])
        # Add edge when cycle continues
        graph.add_edge(
            n_id,
            statements[0],
            label_true='true',
            label_cfg='CFG',
        )
        # Add cycle restart
        graph.add_edge(
            statements[-1],
            n_id,
            label_e='e',
            label_cfg='CFG',
        )
        if n_attrs.get('label_type') == 'WhileStatement':
            # Add edge when loop ends
            graph[n_id][else_id]['label_false'] = 'false'
            graph[n_id][else_id].pop('label_e', None)
        elif n_attrs.get('label_type') == 'DoStatement':
            # Add edge when loop ends
            graph.add_edge(
                statements[-1],
                else_id,
                label_false='false',
                label_cfg='CFG',
            )

        # Find `continue` and `break` statements
        for _statement in nx.dfs_successors(graph,
                                            source=while_block_statement):
            # Prevent the tour from leaving the declaration block
            if _statement == n_id:
                break
            if graph.nodes[_statement].get(
                    'label_type') == 'ContinueStatement':
                graph.add_edge(
                    _statement,
                    n_id,
                    label_continue='continue',
                    label_cfg='CFG',
                )
            elif graph.nodes[_statement].get('label_type') == 'BreakStatement':
                graph.add_edge(
                    _statement,
                    else_id,
                    label_break='break',
                    label_cfg='CFG',
                )


def analyze(graph: nx.OrderedDiGraph) -> None:
    _analyze_if_then_statement(graph)
    _analyze_block_statements(graph)
    _analyze_while_statements(graph)
