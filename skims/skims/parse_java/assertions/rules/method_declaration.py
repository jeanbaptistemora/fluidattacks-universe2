# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
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

    # methodDeclaration = methodModifier* methodHeader methodBody
    match = g.match_ast(graph, n_id, 'MethodHeader')
    if c_id := match['MethodHeader']:
        _method_header(graph, c_id, ctx=ctx)
    else:
        common.warn_not_impl(inspect, n_id=n_id)

    return common.mark_seen(ctx, n_id)


def _method_header(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # methodHeader
    #   : result methodDeclarator throws_?
    #   | typeParameters annotation* result methodDeclarator throws_?
    match = g.match_ast(graph, n_id, 'MethodDeclarator')
    if c_id := match['MethodDeclarator']:
        _method_declarator(graph, c_id, ctx=ctx)
    else:
        common.warn_not_impl(_method_header, n_id=n_id)

    return common.mark_seen(ctx, n_id)


def _method_declarator(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # methodDeclarator = identifier '(' formalParameterList? ')' dims?
    match = g.match_ast(graph, n_id, 'FormalParameterList')
    if c_id := match['FormalParameterList']:
        _formal_parameter_list(graph, c_id, ctx=ctx)
    else:
        common.warn_not_impl(_method_declarator, n_id=n_id)

    return common.mark_seen(ctx, n_id)


def _formal_parameter_list(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    for c_id in g.filter_nodes(
        graph,
        g.adj_ast(graph, n_id, depth=-1),
        g.pred_has_labels(label_type='FormalParameter'),
    ):
        _formal_parameter(graph, c_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)


def _formal_parameter(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    c_ids = g.adj_ast(graph, n_id)

    if (
        len(c_ids) == 2
        and graph.nodes[c_ids[0]]['label_type'] == 'IdentifierRule'
        and graph.nodes[c_ids[1]]['label_type'] == 'IdentifierRule'
    ):
        type_attrs = graph.nodes[c_ids[0]]
        type_attrs_label_text = type_attrs['label_text']
        var_attrs = graph.nodes[c_ids[1]]
        var_attrs_label_text = var_attrs['label_text']

        # Add the variable to the mapping
        ctx['log'].append({
            'type': 'BINDING',
            'target': var_attrs_label_text,
            'target_type': type_attrs_label_text,
        })

        # Taint the variable
        if type_attrs_label_text in {'HttpServletRequest'}:
            ctx['log'].append({
                'type': 'TAINT',
                'target': var_attrs_label_text,
                '__reason__': 'Variable is user controlled',
            })
    else:
        common.warn_not_impl(_formal_parameter, n_id=n_id)

    return common.mark_seen(ctx, n_id)
