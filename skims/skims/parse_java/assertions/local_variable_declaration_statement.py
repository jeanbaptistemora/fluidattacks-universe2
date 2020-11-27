# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
    generic,
)
from utils import (
    graph as g,
)


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # localVariableDeclarationStatement = localVariableDeclaration ';'
    match = g.match_ast(graph, n_id, 'LocalVariableDeclaration')
    if c_id := match['LocalVariableDeclaration']:
        _local_variable_declaration(graph, c_id, ctx=ctx)
    else:
        common.warn_not_impl(inspect, n_id=n_id)

    return common.mark_seen(ctx, n_id)


def _local_variable_declaration(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # variableModifier* unannType variableDeclaratorList
    # Mostly due to reducers this end up being:
    # - CustomUnannArrayType VariableDeclarator
    # - CustomUnannClassOrInterfaceType VariableDeclarator
    # - IdentifierRule VariableDeclarator
    c_ids = g.adj_ast(graph, n_id)

    if (
        len(c_ids) == 2
        # Type
        and graph.nodes[c_ids[0]]['label_type'] in {
            'CustomUnannArrayType',
            'CustomUnannClassOrInterfaceType',
            'VariableDeclarator',
        }
        # Binding
        and graph.nodes[c_ids[1]]['label_type'] == 'VariableDeclarator'
    ):
        _variable_declarator(
            graph,
            c_ids[1],
            ctx=ctx,
            type_attrs_label_text=graph.nodes[c_ids[0]]['label_text'],
        )
    else:
        common.warn_not_impl(_local_variable_declaration, n_id=n_id)

    return common.mark_seen(ctx, n_id)


def _variable_declarator(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
    type_attrs_label_text: str,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # variableDeclaratorId ('=' variableInitializer)?
    match = g.match_ast(graph, n_id, 'IdentifierRule', 'ASSIGN')

    if (
        match['IdentifierRule']
        and match['ASSIGN']
        and (src_id := match['__0__'])
    ):
        src_ctx = generic.inspect(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        # Add the variable to the mapping
        ctx['log'].append({
            'source': src_ctx['log'],
            'type': 'BINDING',
            'var': graph.nodes[match['IdentifierRule']]['label_text'],
            'var_type': type_attrs_label_text,
        })
    else:
        common.warn_not_impl(_local_variable_declaration, n_id=n_id)

    return common.mark_seen(ctx, n_id)
