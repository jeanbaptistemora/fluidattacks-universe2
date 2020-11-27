"""Walk the graph and append edges with the possible code execution flow."""

# Standar library
from typing import (
    Iterator,
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

# Constants
ALWAYS = dict(label_e='e', label_cfg='CFG')
MAYBE = dict(label_m='m', label_cfg='CFG')
BREAK = dict(label_break='break', **ALWAYS)
CONTINUE = dict(label_continue='continue', **ALWAYS)
FALSE = dict(label_false='false', label_cfg='CFG')
TRUE = dict(label_true='true', label_cfg='CFG')


def _pred_ast_types(
    graph: nx.DiGraph,
    n_id: str,
    *label_types: str,
    depth: int = 1,
) -> Iterator[str]:
    for node in g.pred_lazy(graph, n_id, depth, label_ast='AST'):
        if any(
            g.has_labels(graph.nodes[node], label_type=label)
                for label in label_types):
            yield node


def _loop_statements(graph: nx.DiGraph) -> None:
    for n_id in (
        key for key, value in graph.nodes.items()
            if value['label_type'] in {'BasicForStatement', 'WhileStatement'}):

        loop_block_statement = g.adj_ast(
            graph,
            n_id,
            depth=1,
            label_type='Block',
        )[0]
        graph[n_id][loop_block_statement]['label_true'] = 'true'
        graph[n_id][loop_block_statement].update(**ALWAYS)

        # BlockStatements
        blockstatements = g.adj_ast(
            graph,
            loop_block_statement,
            depth=1,
            label_type='BlockStatements',
        )
        # BlockStatements may not exists, it is an ExpresionStatement when the
        # Block has only one statement
        statements = g.adj(graph, blockstatements[0]) if blockstatements else (
            g.adj(graph, loop_block_statement)[1], )

        # Add cycle restart
        graph.add_edge(statements[-1], n_id, **ALWAYS)

        else_id = g.adj(graph, n_id)[-1]
        else_parent = graph.nodes[else_id]['label_parent_ast']
        # This statement can be the last in the BlockStatement
        # else_id can be a children directly of loop statement
        else_in_block = else_parent != n_id
        if else_in_block:
            # Add edge when loop ends
            graph[n_id][else_id]['label_false'] = 'false'
            graph[n_id][else_id].pop('label_e', None)


def _do_statement(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='DoStatement'
    )):
        block_statement = g.adj(graph, n_id)[1]
        graph[n_id][block_statement].update(**ALWAYS)

        # BlockStatements
        blockstatements = g.adj_ast(
            graph,
            block_statement,
            depth=1,
            label_type='BlockStatements',
        )
        # BlockStatements may not exists, it is an ExpresionStatement when the
        # Block has only one statement
        statements = g.adj(graph, blockstatements[0]) if blockstatements else (
            g.adj(graph, block_statement)[1], )

        # Add loop restart
        graph.add_edge(statements[-1], n_id, **TRUE)

        else_id = g.adj(graph, n_id)[-1]
        else_parent = graph.nodes[else_id]['label_parent_ast']
        else_in_block = else_parent != n_id
        # This statement can be the last in the BlockStatement
        # else_id can be a children directly of loop statement
        if else_in_block:
            # Add edge when loop ends
            graph.add_edge(statements[-1], else_id, **FALSE)


def _continue(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='ContinueStatement'
    )):
        for loop in _pred_ast_types(
            graph,
            n_id,
            'DoStatement',
            'BasicForStatement',
            'WhileStatement',
            depth=-1,
        ):
            graph.add_edge(n_id, loop, **CONTINUE)
            break


def _break(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='BreakStatement'
    )):
        for loop in _pred_ast_types(
            graph,
            n_id,
            'DoStatement',
            'BasicForStatement',
            'WhileStatement',
            'SwitchStatement',
            depth=-1,
        ):
            else_id = g.adj(graph, loop)[-1]
            else_parent = graph.nodes[else_id]['label_parent_ast']
            else_in_block = else_parent != loop
            # This statement can be the last in the BlockStatement
            # else_id can be a children directly of loop statement
            if else_in_block:
                # Add edge when loop ends
                graph.add_edge(n_id, else_id, **BREAK)
            break


def _method_declaration(graph: nx.DiGraph) -> None:
    # Iterate all MethodDeclaration nodes
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='MethodDeclaration',
    )):
        # MethodDeclaration = MethodModifier MethodHeader Block
        block_id = g.adj(graph, n_id)[-1]
        graph.add_edge(n_id, block_id, **ALWAYS)


def _block(graph: nx.DiGraph) -> None:
    # Iterate all Block nodes
    for block_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='Block',
    )):
        block_c_id = g.adj(graph, block_id)[1]
        graph.add_edge(block_id, block_c_id, **ALWAYS)


def _block_statements(graph: nx.DiGraph) -> None:
    # Iterate all Block nodes
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] in {
            'BlockStatements',
            'ExpressionStatement',
        }:
            # Statements = step1 step2 ...
            stmt_ids = g.adj(graph, n_id)

            # Walk the Statements
            for first, _, (stmt_a_id, stmt_b_id) in mark_ends(
                pairwise(stmt_ids),
            ):
                if first:
                    # Link Block to first Statement
                    graph.add_edge(n_id, stmt_a_id, **ALWAYS)

                if 'SEMI' in {
                    graph.nodes[stmt_b_id]['label_type'],
                    graph.nodes[stmt_a_id]['label_type'],
                }:
                    continue

                graph.add_edge(stmt_a_id, stmt_b_id, **ALWAYS)


def _if_then_statement(graph: nx.DiGraph) -> None:
    # Iterate nodes
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] in {
            'IfThenStatement',
            'IfThenElseStatement',
        }:
            # Find the IfThenStatement `then` node
            c_ids = g.adj(graph, n_id)
            graph.add_edge(n_id, c_ids[4], **TRUE)

            # Find the IfThenElseStatement `else` node
            if n_attrs['label_type'] == 'IfThenElseStatement':
                graph.add_edge(n_id, c_ids[6], **FALSE)


def _switch_statements(graph: nx.DiGraph) -> None:
    # Iterate all switch statements
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='SwitchStatement',
    )):
        _switch_block = g.adj(graph, n_id)[4]
        graph.add_edge(n_id, _switch_block, **ALWAYS)

        block_statements_groups = g.adj_ast(
            graph,
            _switch_block,
            depth=1,
            label_type='SwitchBlockStatementGroup',
        )
        last_statement = None
        for statement_group in block_statements_groups:
            graph.add_edge(_switch_block, statement_group, **ALWAYS)
            block_statements = g.adj(graph, statement_group)[1]
            if last_statement:
                graph.add_edge(last_statement, statement_group, **ALWAYS)

            graph.add_edge(statement_group, block_statements, **TRUE)
            if graph.nodes[block_statements][
                    'label_type'] == 'BlockStatements':
                statements = g.adj(graph, block_statements)
            else:
                statements = (g.adj(graph, block_statements)[0], )

            if graph.nodes[statements[-1]]['label_type'] == 'BreakStatement':
                last_statement = None
            else:
                # if the block does not end with BreakStatement, the following
                # case is executed
                last_statement = statements[-1]


def _try_statement(graph: nx.DiGraph) -> None:
    # Iterate all TryStatement nodes
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='TryStatement',
    )):
        # Strain the childs over the following node types
        childs = g.match_ast(
            graph,
            n_id,
            # Components in order
            'TRY',
            'ResourceSpecification',
            'Block',
            'Catches',
            'CatchClause',
            'Finally_',
            'SEMI',
        )

        # Initialize by linking the parent to the first executed node
        p_id = n_id

        # If present, this is always evaluated
        if c_id := childs['ResourceSpecification']:
            graph.add_edge(p_id, c_id, **ALWAYS)
            p_id = c_id

        # This is always present and evaluated
        if c_id := childs['Block']:
            graph.add_edge(p_id, c_id, **ALWAYS)
            p_id = c_id

        # Only if something inside the Block throwed an exception
        if c_id := childs['CatchClause']:
            graph.add_edge(p_id, c_id, **MAYBE)
            p_id = c_id

        # Only if something inside the Block throwed an exception
        if c_id := childs['Catches']:
            # Link to the CatchClause nodes
            for c_c_id in g.adj(graph, c_id):
                graph.add_edge(p_id, c_c_id, **MAYBE)
            p_id = c_id

        # If Present finally is always executed
        if c_id := childs['Finally_']:
            graph.add_edge(p_id, c_id, **ALWAYS)
            p_id = c_id


def _try_statement_catch_clause(graph: nx.DiGraph) -> None:
    # Iterate all CatchClause nodes
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CatchClause',
    )):
        # CatchClause = CATCH ( CatchFormalParameter ) BLOCK
        c_ids = g.adj(graph, n_id)
        graph.add_edge(n_id, c_ids[4], **ALWAYS)


def _primary(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='Primary',
    )):
        invocations = g.adj_ast(graph, n_id)
        graph.add_edge(n_id, invocations[0], **ALWAYS)
        for s_id, d_id in pairwise(invocations):
            graph.add_edge(s_id, d_id, **ALWAYS)


def _link_to_parent(graph: nx.DiGraph, label_type: str) -> None:
    for n_id in g.filter_nodes(
        graph, graph.nodes, g.pred_has_labels(label_type=label_type),
    ):
        graph.add_edge(graph.nodes[n_id]['label_parent_ast'], n_id, **ALWAYS)


def analyze(graph: nx.DiGraph) -> None:
    _method_declaration(graph)
    _block(graph)
    _block_statements(graph)
    _try_statement(graph)
    _try_statement_catch_clause(graph)
    _if_then_statement(graph)
    _loop_statements(graph)
    _do_statement(graph)
    _switch_statements(graph)
    _continue(graph)
    _break(graph)
    _primary(graph)

    # Single evaluations
    for label_type in (
        'CustomClassInstanceCreationExpression_lfno_primary',
        'LocalVariableDeclaration',
        'VariableDeclarator',
        'Primary',
    ):
        _link_to_parent(graph, label_type)
