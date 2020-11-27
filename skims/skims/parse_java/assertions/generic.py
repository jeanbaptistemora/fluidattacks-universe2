# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
    local_variable_declaration_statement,
    method_declaration,
)

# Constants
_UNINTERESTING_NODES = {
    'Block',
    'BlockStatements',
    'SEMI',
}


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    n_attrs_label_type = graph.nodes[n_id]['label_type']

    if n_attrs_label_type == 'MethodDeclaration':
        method_declaration.inspect(graph, n_id, ctx=ctx)
    elif n_attrs_label_type == 'ExpressionStatement':
        pass
    elif n_attrs_label_type == 'LocalVariableDeclarationStatement':
        local_variable_declaration_statement.inspect(graph, n_id, ctx=ctx)
    elif n_attrs_label_type in _UNINTERESTING_NODES:
        pass
    else:
        raise NotImplementedError(n_attrs_label_type)

    return ctx
