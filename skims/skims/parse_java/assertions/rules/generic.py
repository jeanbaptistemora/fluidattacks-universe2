# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
)
from parse_java.assertions.rules import (
    additive_expression,
    argument_list,
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

    if common.already_seen(ctx, n_id):
        return common.mark_seen(ctx, n_id)

    n_attrs_label_type = graph.nodes[n_id]['label_type']

    if n_attrs_label_type in _UNINTERESTING_NODES:
        return common.mark_seen(ctx, n_id)

    for types, inspector in (
        ({'AdditiveExpression'},
         additive_expression.inspect),
        ({'ArgumentList'},
         argument_list.inspect),
        ({'CustomClassInstanceCreationExpression_lfno_primary'},
         custom_class_instance_creation_expression_lfno_primary.inspect),
        ({'CustomMethodInvocation',
          'CustomMethodInvocation_lfno_primary'},
         custom_method_invocation.inspect),
        ({'ExpressionStatement'},
         expression_statement.inspect),
        ({'LocalVariableDeclarationStatement'},
         local_variable_declaration_statement.inspect),
        ({'MethodDeclaration'},
         method_declaration.inspect),
        ({'CustomExpressionName',
          'IdentifierRule',
          'StringLiteral'},
         string_literal.inspect),
    ):
        if n_attrs_label_type in types:
            inspector(graph, n_id, ctx=ctx)
            return common.mark_seen(ctx, n_id)

    common.warn_not_impl(inspect, n_id=n_id)
    return common.mark_seen(ctx, n_id)
