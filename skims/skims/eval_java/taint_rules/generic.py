# Local libraries
from eval_java.model import (
    ExpressionConditional,
    StatementAdd,
    StatementAssignment,
    StatementCast,
    StatementClassInstantiation,
    StatementCustomMethodInvocation,
    StatementDeclaration,
    StatementLiteral,
    StatementLookup,
    StatementPass,
    StatementPrimary,
    Statements,
)
from eval_java.taint_rules import (
    add,
    assignment,
    call,
    cast,
    class_instantiation,
    declaration,
    expression_conditional,
    ignore,
    literal,
    lookup,
    primary,
)


TAINTERS = {
    ExpressionConditional: expression_conditional.taint,
    StatementAdd: add.taint,
    StatementAssignment: assignment.taint,
    StatementCast: cast.taint,
    StatementClassInstantiation: class_instantiation.taint,
    StatementCustomMethodInvocation: call.taint,
    StatementDeclaration: declaration.taint,
    StatementLiteral: literal.taint,
    StatementLookup: lookup.taint,
    StatementPass: ignore.taint,
    StatementPrimary: primary.taint,
}


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False
        TAINTERS[type(statement)](statements, index)
