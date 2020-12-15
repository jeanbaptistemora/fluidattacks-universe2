# Local libraries
from eval_java.model import (
    ExpressionConditional,
    ExpressionRelational,
    StatementAdd,
    StatementAssignment,
    StatementCast,
    StatementClassInstantiation,
    StatementCustomMethodInvocation,
    StatementCustomMethodInvocationChain,
    StatementDeclaration,
    StatementLiteral,
    StatementLookup,
    StatementPass,
    StatementPrimary,
    Statements,
)
from eval_java.eval_rules import (
    add,
    assignment,
    call,
    call_chain,
    common,
    cast,
    class_instantiation,
    declaration,
    expression_conditional,
    expression_relational,
    ignore,
    literal,
    lookup,
    primary,
)


EVALUATORS = {
    ExpressionConditional: expression_conditional.evaluate,
    ExpressionRelational: expression_relational.evaluate,
    StatementAdd: add.evaluate,
    StatementAssignment: assignment.evaluate,
    StatementCast: cast.evaluate,
    StatementClassInstantiation: class_instantiation.evaluate,
    StatementCustomMethodInvocation: call.evaluate,
    StatementCustomMethodInvocationChain: call_chain.evaluate,
    StatementDeclaration: declaration.evaluate,
    StatementLiteral: literal.evaluate,
    StatementLookup: lookup.evaluate,
    StatementPass: ignore.evaluate,
    StatementPrimary: primary.evaluate,
}


def evaluate(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False

        # Default value propagation
        stack = common.read_stack(statements, index)
        if len(stack) == 1:
            statement.meta.value = stack[0].meta.value

        EVALUATORS[type(statement)](statements, index)
