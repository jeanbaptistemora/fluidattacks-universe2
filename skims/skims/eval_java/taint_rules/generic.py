# Local libraries
from eval_java.model import (
    StatementAdd,
    StatementAssignment,
    StatementCast,
    StatementClassInstantiation,
    StatementCustomMethodInvocation,
    StatementDeclaration,
    StatementLiteral,
    StatementLookup,
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
    literal,
    lookup,
    primary,
)


TAINTERS = {
    StatementAdd: add.taint,
    StatementAssignment: assignment.taint,
    StatementCast: cast.taint,
    StatementClassInstantiation: class_instantiation.taint,
    StatementCustomMethodInvocation: call.taint,
    StatementDeclaration: declaration.taint,
    StatementLiteral: literal.taint,
    StatementLookup: lookup.taint,
    StatementPrimary: primary.taint,
}


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False
        TAINTERS[type(statement)](statements, index)
