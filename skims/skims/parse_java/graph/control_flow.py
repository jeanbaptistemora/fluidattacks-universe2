"""Walk the graph and append edges with the possible code execution flow."""
# Standar libraries
from typing import (
    Any,
    Tuple,
)

# Third party libraries
import networkx as nx
from more_itertools import (
    mark_ends,
    pairwise,
)
from utils import (
    graph as g,
)
from utils.graph import (
    has_labels,
)


# Constants
ALWAYS = dict(label_e='e', label_cfg='CFG')
BREAK = dict(label_break='break', **ALWAYS)
CONTINUE = dict(label_continue='continue', **ALWAYS)
FALSE = dict(label_false='false', label_cfg='CFG')
TRUE = dict(label_true='true', label_cfg='CFG')


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


def _loop_statements(graph: nx.OrderedDiGraph) -> None:
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
        graph.add_edge(n_id, statements[0], **TRUE)
        # Add cycle restart
        graph.add_edge(statements[-1], n_id, **ALWAYS)

        if n_attrs['label_type'] == 'WhileStatement':
            # Add edge when loop ends
            graph[n_id][else_id]['label_false'] = 'false'
            graph[n_id][else_id].pop('label_e', None)
        elif n_attrs['label_type'] == 'DoStatement':
            # Add edge when loop ends
            graph.add_edge(statements[-1], else_id, **FALSE)

        # Find `continue` and `break` statements
        for _statement in nx.dfs_successors(
            graph,
            source=loop_block_statement,
        ):
            # Prevent the tour from leaving the declaration block
            if _statement == n_id:
                break
            if graph.nodes[_statement]['label_type'] == 'ContinueStatement':
                graph.add_edge(_statement, n_id, **CONTINUE)
            elif graph.nodes[_statement]['label_type'] == 'BreakStatement':
                graph.add_edge(_statement, else_id, **BREAK)


def _method_declaration(graph: nx.OrderedDiGraph) -> None:
    # Iterate all MethodDeclaration nodes
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='MethodDeclaration',
    )):
        # MethodDeclaration = MethodModifier MethodHeader Block
        block_id = g.adj(graph, n_id)[2]
        graph.add_edge(n_id, block_id, **ALWAYS)


def _block_statements(graph: nx.OrderedDiGraph) -> None:
    # Iterate all Block nodes
    for block_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='Block',
    )):
        # Block = { BasicForStatement }
        # Block = { BlockStatement }
        # Block = { ExpressionStatement }
        # Block = { IfThenStatement }
        block_c_id = g.adj(graph, block_id)[1]
        graph.add_edge(block_id, block_c_id, **ALWAYS)

        if graph.nodes[block_c_id]['label_type'] in {
            'BlockStatement',
            'ExpressionStatement',
        }:
            # Statements = step1 step2 ...
            stmt_ids = g.adj(graph, block_c_id)

            # Walk the Statements
            for first, _, (stmt_a_id, stmt_b_id) in mark_ends(
                pairwise(stmt_ids),
            ):
                if first:
                    # Link Block to first Statement
                    graph.add_edge(block_c_id, stmt_a_id, **ALWAYS)

                # Link Statement[i] to Statement[i + 1]
                graph.add_edge(stmt_a_id, stmt_b_id, **ALWAYS)


def _if_then_statement(graph: nx.OrderedDiGraph) -> None:
    # Iterate nodes
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] in {'IfThenStatement', 'IfThenElseStatement'}:
            # Find the IfThenStatement `then` node
            c_ids = g.adj(graph, n_id)
            graph.add_edge(n_id, c_ids[4], **TRUE)

            # Find the IfThenElseStatement `else` node
            if n_attrs['label_type'] == 'IfThenElseStatement':
                graph.add_edge(n_id, c_ids[6], **FALSE)


def analyze(graph: nx.OrderedDiGraph) -> None:
    _method_declaration(graph)
    _block_statements(graph)
    _if_then_statement(graph)
    _loop_statements(graph)
