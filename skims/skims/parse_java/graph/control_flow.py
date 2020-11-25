"""Walk the graph and append edges with the possible code execution flow."""
# Standar libraries
from typing import (
    Any,
    Dict,
    Optional,
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
MAYBE = dict(label_m='m', label_cfg='CFG')
BREAK = dict(label_break='break', **ALWAYS)
CONTINUE = dict(label_continue='continue', **ALWAYS)
FALSE = dict(label_false='false', label_cfg='CFG')
TRUE = dict(label_true='true', label_cfg='CFG')


def _get_successors_by_label(
    graph: nx.DiGraph,
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


def _match_childs_over_template(
    graph: nx.DiGraph,
    n_id: str,
    template_keys: Tuple[str, ...],
) -> Dict[str, Optional[str]]:
    template: Dict[str, Optional[str]] = dict.fromkeys(template_keys)

    for c_id in g.adj(graph, n_id, label_ast='AST'):
        c_type = graph.nodes[c_id]['label_type']
        if c_type in template:
            template[c_type] = c_id
        else:
            raise NotImplementedError(c_type)

    return template


def _loop_statements(graph: nx.DiGraph) -> None:
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] not in {
            'BasicForStatement',
            'DoStatement',
            'WhileStatement',
        }:
            continue

        _loop_block_statement: Tuple[str, ...] = _get_successors_by_label(
            graph,
            n_id,
            depth_limit=2,
            label_type='BlockStatement',
        )
        if _loop_block_statement:
            loop_block_statement: str = _loop_block_statement[0]
            statements: Tuple[str, ...] = g.adj(graph, loop_block_statement)
        else:
            # Some loops only have a single statement, the BlockStatement
            # does not appear in the graph
            block = _get_successors_by_label(
                graph,
                n_id,
                depth_limit=1,
                label_type='Block',
            )[0]
            statements = (g.adj(graph, block)[1], )
            loop_block_statement = block

        # Add edge when cycle continues
        graph.add_edge(n_id, statements[0], **TRUE)
        # Add cycle restart
        graph.add_edge(statements[-1], n_id, **ALWAYS)

        else_id = g.adj(graph, n_id)[-1]
        else_parent = tuple(graph.predecessors(else_id))[0]
        # This statement can be the last in the BlockStatement
        # else_id can be a children directly of loop statement
        else_in_block = graph.nodes[else_parent][
            'label_type'] == 'BlockStatement'

        if n_attrs['label_type'] == 'WhileStatement' and else_in_block:
            # Add edge when loop ends
            graph[n_id][else_id]['label_false'] = 'false'
            graph[n_id][else_id].pop('label_e', None)
        elif n_attrs['label_type'] == 'DoStatement' and else_in_block:
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
            elif graph.nodes[_statement][
                    'label_type'] == 'BreakStatement' and else_in_block:
                graph.add_edge(_statement, else_id, **BREAK)


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

                # Link Statement[i] to Statement[i + 1]
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
    for n_id, n_attrs in graph.nodes.items():
        if n_attrs['label_type'] == 'SwitchStatement':
            block_statement_cases = _get_successors_by_label(
                graph=graph,
                source=n_id,
                depth_limit=3,
                label_type='SwitchBlockStatementGroup',
            )[0]
            for case in g.adj(graph, block_statement_cases):
                block_statements = _get_successors_by_label(
                    graph,
                    case,
                    depth_limit=2,
                    label_type='BlockStatement',
                )
                if block_statements:
                    statements = g.adj(graph, block_statements[0])
                else:
                    statements = (g.adj(graph, case)[-1], )

                graph.add_edge(n_id, statements[0], **ALWAYS)
                else_block = g.adj(graph, n_id)[-1]
                else_parent = tuple(graph.predecessors(else_block))[0]
                # This statement can be the last in the BlockStatement
                else_in_block = graph.nodes[else_parent][
                    'label_type'] == 'BlockStatement'
                if else_in_block:
                    graph.add_edge(statements[-1], else_block, **ALWAYS)


def _try_statement(graph: nx.DiGraph) -> None:
    # Iterate all TryStatement nodes
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='TryStatement',
    )):
        # Strain the childs over the following node types
        childs = _match_childs_over_template(graph, n_id, (
            # Components in order
            'TRY',
            'ResourceSpecification',
            'Block',
            'Catches',
            'CatchClause',
            'Finally_',
            'SEMI',
        ))

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
    _switch_statements(graph)

    # Single evaluations
    _link_to_parent(graph, 'ClassInstanceCreationExpression_lfno_primary')
    _link_to_parent(graph, 'LocalVariableDeclaration')
    _link_to_parent(graph, 'VariableDeclarator')
