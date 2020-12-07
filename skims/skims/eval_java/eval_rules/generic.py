# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    additive_expression,
    argument_list,
    assignment,
    common,
    custom_class_instance_creation_expression_lfno_primary,
    custom_method_invocation,
    enhanced_for_statement,
    expression_statement,
    identifier_rule,
    literal,
    local_variable_declaration_statement,
    method_declaration,
    primary,
)
from eval_java.model import (
    Context,
    OptionalContext,
)

# Constants
_UNINTERESTING_NODES = {
    'Block',
    'BlockStatements',
    'BreakStatement',
    'IfThenElseStatement',
    'IfThenStatement',
    'ResourceSpecification',
    'SEMI',
    'TryStatement',
}


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    # Check if we already extracted context from this node
    if n_id in ctx.seen:
        return common.mark_seen(ctx, n_id)

    n_attrs_label_type = graph.nodes[n_id]['label_type']

    if n_attrs_label_type in _UNINTERESTING_NODES:
        return common.mark_seen(ctx, n_id)

    for types, evaluator in (
        ({'AdditiveExpression'},
         additive_expression.evaluate),
        ({'ArgumentList'},
         argument_list.evaluate),
        ({'Assignment'},
         assignment.evaluate),
        ({'CustomClassInstanceCreationExpression_lfno_primary'},
         custom_class_instance_creation_expression_lfno_primary.evaluate),
        ({'BooleanLiteral',
          'CustomExpressionName',
          'NullLiteral',
          'StringLiteral'},
         literal.evaluate),
        ({'CustomArrayAccess_lfno_primary',
          'IdentifierRule'},
         identifier_rule.evaluate),
        ({'CustomMethodInvocation',
          'CustomMethodInvocation_lfno_primary',
          'CustomMethodInvocation_lf_primary'},
         custom_method_invocation.evaluate),
        ({'EnhancedForStatement'},
         enhanced_for_statement.evaluate),
        ({'ExpressionStatement'},
         expression_statement.evaluate),
        ({'LocalVariableDeclarationStatement'},
         local_variable_declaration_statement.evaluate),
        ({'MethodDeclaration'},
         method_declaration.evaluate),
        ({'Primary'},
         primary.evaluate),
    ):
        if n_attrs_label_type in types:
            evaluator(graph, n_id, ctx=ctx)
            return common.mark_seen(ctx, n_id)

    common.not_implemented(evaluate, n_id, ctx=ctx)
    return common.mark_seen(ctx, n_id)
