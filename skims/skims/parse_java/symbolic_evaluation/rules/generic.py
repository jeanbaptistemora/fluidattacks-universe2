# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)
from parse_java.symbolic_evaluation.rules import (
    additive_expression,
    argument_list,
    custom_class_instance_creation_expression_lfno_primary,
    custom_method_invocation,
    expression_statement,
    identifier_rule,
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


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    # Check if we already extracted context from this node
    if n_id in ctx['seen']:
        return common.mark_seen(ctx, n_id)

    n_attrs_label_type = graph.nodes[n_id]['label_type']

    if n_attrs_label_type in _UNINTERESTING_NODES:
        return common.mark_seen(ctx, n_id)

    for types, evaluator in (
        ({'AdditiveExpression'},
         additive_expression.evaluate),
        ({'ArgumentList'},
         argument_list.evaluate),
        ({'CustomClassInstanceCreationExpression_lfno_primary'},
         custom_class_instance_creation_expression_lfno_primary.evaluate),
        ({'CustomMethodInvocation',
          'CustomMethodInvocation_lfno_primary'},
         custom_method_invocation.evaluate),
        ({'ExpressionStatement'},
         expression_statement.evaluate),
        ({'IdentifierRule'},
         identifier_rule.evaluate),
        ({'LocalVariableDeclarationStatement'},
         local_variable_declaration_statement.evaluate),
        ({'MethodDeclaration'},
         method_declaration.evaluate),
        ({'CustomExpressionName',
          'StringLiteral'},
         string_literal.evaluate),
    ):
        if n_attrs_label_type in types:
            evaluator(graph, n_id, ctx=ctx)
            return common.mark_seen(ctx, n_id)

    common.not_implemented(evaluate, n_id, ctx=ctx)
    return common.mark_seen(ctx, n_id)
