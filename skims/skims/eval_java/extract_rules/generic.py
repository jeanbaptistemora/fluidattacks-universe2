# Third party libraries
import networkx as nx

# Local libraries
from eval_java.extract_rules import (
    additive_expression,
    argument_list,
    assignment,
    basic_for_statement,
    cast_expression,
    common,
    conditional_expression,
    custom_class_instance_creation_expression_lfno_primary,
    custom_method_invocation,
    enhanced_for_statement,
    expression_statement,
    identifier_rule,
    if_statement,
    literal,
    local_variable_declaration_statement,
    method_declaration,
    primary,
    relational_expression,
    resource_specification,
    unary_expression,
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
    'ContinueStatement',
    'ReturnStatement',
    'SEMI',
    'SwitchStatement',
    'TryStatement',
    'WhileStatement',
}


def extract(
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
         additive_expression.extract),
        ({'ArgumentList'},
         argument_list.extract),
        ({'Assignment'},
         assignment.extract),
        ({'BasicForStatement'},
         basic_for_statement.extract),
        ({'BooleanLiteral',
          'CharacterLiteral',
          'CustomExpressionName',
          'CustomNumericLiteral',
          'FloatingPointLiteral',
          'IntegerLiteral',
          'NullLiteral',
          'StringLiteral',
          'THIS'},
         literal.extract),
        ({'CastExpression'},
         cast_expression.extract),
        ({'ConditionalExpression'},
         conditional_expression.extract),
        ({'CustomClassInstanceCreationExpression_lfno_primary'},
         custom_class_instance_creation_expression_lfno_primary.extract),
        ({'CustomArrayAccess_lfno_primary',
          'IdentifierRule'},
         identifier_rule.extract),
        ({'CustomMethodInvocation',
          'CustomMethodInvocation_lfno_primary',
          'CustomMethodInvocation_lf_primary'},
         custom_method_invocation.extract),
        ({'EnhancedForStatement'},
         enhanced_for_statement.extract),
        ({'EqualityExpression',
          'RelationalExpression'},
         relational_expression.extract),
        ({'ExpressionStatement'},
         expression_statement.extract),
        ({'IfThenElseStatement',
          'IfThenStatement'},
         if_statement.extract),
        ({'LocalVariableDeclarationStatement'},
         local_variable_declaration_statement.extract),
        ({'MethodDeclaration'},
         method_declaration.extract),
        ({'Primary'},
         primary.extract),
        ({'ResourceSpecification'},
         resource_specification.extract),
        ({'UnaryExpressionNotPlusMinus'},
         unary_expression.extract)
    ):
        if n_attrs_label_type in types:
            evaluator(graph, n_id, ctx=ctx)
            return common.mark_seen(ctx, n_id)

    common.not_implemented(extract, n_id, ctx=ctx)
    return common.mark_seen(ctx, n_id)
