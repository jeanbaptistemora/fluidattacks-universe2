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
from utils import (
    graph as g,
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
        if n_attrs['label_type'] in {'IfThenStatement', 'IfThenElseStatement'}:
            # Find the IfThenStatement `then` node
            c_ids = g.adj(graph, n_id)
            graph.add_edge(
                n_id,
                c_ids[4],
                label_cfg='CFG',
                label_true='true',
            )

            # Find the IfThenElseStatement `else` node
            if n_attrs['label_type'] == 'IfThenElseStatement':
                graph.add_edge(
                    n_id,
                    c_ids[6],
                    label_cfg='CFG',
                    label_false='false',
                )


def _analyze_block_statements(graph: nx.OrderedDiGraph) -> None:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] == 'BlockStatement':
            for a_id, b_id in windowed(g.adj(graph, n_id), 2):
                graph.add_edge(
                    a_id,
                    b_id,
                    label_e='e',
                    label_cfg='CFG',
                )


def _analyze_loop_statements(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] not in {
            'BasicForStatement',
            'DoStatement',
            'WhileStatement',
        }:
            continue

        else_id = tuple(graph.adj[n_id])[-1]
        loop_block_statement = _get_successors_by_label(
            graph,
            n_id,
            depth_limit=2,
            label_type='BlockStatement',
        )
        if loop_block_statement:
            loop_block_statement = loop_block_statement[0]
            statements = tuple(graph.adj[loop_block_statement])
        else:
            # Some loops only have a single statement, the BlockStatement
            # does not appear in the graph
            block = _get_successors_by_label(
                graph,
                n_id,
                depth_limit=1,
                label_type='Block',
            )[0]
            statements = (tuple(graph.adj[block])[-1], )
            loop_block_statement = block

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
        if n_attrs['label_type'] == 'WhileStatement':
            # Add edge when loop ends
            graph[n_id][else_id]['label_false'] = 'false'
            graph[n_id][else_id].pop('label_e', None)
        elif n_attrs['label_type'] == 'DoStatement':
            # Add edge when loop ends
            graph.add_edge(
                statements[-1],
                else_id,
                label_false='false',
                label_cfg='CFG',
            )

        # Find `continue` and `break` statements
        for _statement in nx.dfs_successors(
            graph,
            source=loop_block_statement,
        ):
            # Prevent the tour from leaving the declaration block
            if _statement == n_id:
                break
            if graph.nodes[_statement]['label_type'] == 'ContinueStatement':
                graph.add_edge(
                    _statement,
                    n_id,
                    label_continue='continue',
                    label_cfg='CFG',
                )
            elif graph.nodes[_statement]['label_type'] == 'BreakStatement':
                graph.add_edge(
                    _statement,
                    else_id,
                    label_break='break',
                    label_cfg='CFG',
                )


def analyze(graph: nx.OrderedDiGraph) -> None:
    _analyze_if_then_statement(graph)
    _analyze_block_statements(graph)
    _analyze_loop_statements(graph)
