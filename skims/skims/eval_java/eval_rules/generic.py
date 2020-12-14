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


TAINTERS = {
    ExpressionConditional: expression_conditional.taint,
    ExpressionRelational: expression_relational.taint,
    StatementAdd: add.taint,
    StatementAssignment: assignment.taint,
    StatementCast: cast.taint,
    StatementClassInstantiation: class_instantiation.taint,
    StatementCustomMethodInvocation: call.taint,
    StatementCustomMethodInvocationChain: call_chain.taint,
    StatementDeclaration: declaration.taint,
    StatementLiteral: literal.taint,
    StatementLookup: lookup.taint,
    StatementPass: ignore.taint,
    StatementPrimary: primary.taint,
}


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False

        # Default value propagation
        stack = common.read_stack(statements, index)
        if len(stack) == 1:
            statement.meta.value = stack[0].meta.value

        TAINTERS[type(statement)](statements, index)
