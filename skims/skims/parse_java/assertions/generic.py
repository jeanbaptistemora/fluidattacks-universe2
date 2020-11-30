# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
    custom_class_instance_creation_expression_lfno_primary,
    custom_method_invocation,
    expression_statement,
    local_variable_declaration_statement,
    method_declaration,
    string_literal,
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

    type_ = graph.nodes[n_id]['label_type']

    if common.already_seen(ctx, n_id):
        pass
    elif type_ == 'CustomClassInstanceCreationExpression_lfno_primary':
        custom_class_instance_creation_expression_lfno_primary.inspect(
            graph, n_id, ctx=ctx,
        )
    elif type_ in {
        'CustomMethodInvocation',
        'CustomMethodInvocation_lfno_primary',
    }:
        custom_method_invocation.inspect(graph, n_id, ctx=ctx)
    elif type_ == 'ExpressionStatement':
        expression_statement.inspect(graph, n_id, ctx=ctx)
    elif type_ == 'LocalVariableDeclarationStatement':
        local_variable_declaration_statement.inspect(graph, n_id, ctx=ctx)
    elif type_ == 'MethodDeclaration':
        method_declaration.inspect(graph, n_id, ctx=ctx)
    elif type_ == 'StringLiteral':
        string_literal.inspect(graph, n_id, ctx=ctx)
    elif type_ in _UNINTERESTING_NODES:
        pass
    else:
        common.warn_not_impl(inspect, n_id=n_id)

    return common.mark_seen(ctx, n_id)
