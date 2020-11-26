# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    types,
)
from utils import (
    graph as g,
)


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: types.Context
) -> None:
    # methodDeclaration = methodModifier* methodHeader methodBody
    match = g.match_ast(graph, n_id, 'MethodHeader')
    if c_id := match['MethodHeader']:
        _method_header(graph, c_id, ctx=ctx)


def _method_header(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: types.Context
) -> None:
    # methodHeader
    #   : result methodDeclarator throws_?
    #   | typeParameters annotation* result methodDeclarator throws_?
    match = g.match_ast(graph, n_id, 'MethodDeclarator')
    if c_id := match['MethodDeclarator']:
        _method_declarator(graph, c_id, ctx=ctx)


def _method_declarator(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: types.Context
) -> None:
    # methodDeclarator = identifier '(' formalParameterList? ')' dims?
    match = g.match_ast(graph, n_id, 'FormalParameterList')
    if c_id := match['FormalParameterList']:
        _formal_parameter_list(graph, c_id, ctx=ctx)


def _formal_parameter_list(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: types.Context
) -> None:
    for c_id in g.filter_nodes(
        graph,
        g.adj_ast(graph, n_id, depth=-1),
        g.pred_has_labels(label_type='FormalParameter'),
    ):
        _formal_parameter(graph, c_id, ctx=ctx)


def _formal_parameter(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: types.Context
) -> None:
    c_ids = g.adj_ast(graph, n_id)

    if (
        len(c_ids) == 2
        and graph.nodes[c_ids[0]]['label_type'] == 'IdentifierRule'
        and graph.nodes[c_ids[1]]['label_type'] == 'IdentifierRule'
    ):
        type_attrs = graph.nodes[c_ids[0]]
        var_attrs = graph.nodes[c_ids[1]]

        ctx['vars'][var_attrs['label_text']] = {
            'type': type_attrs['label_text'],
        }
