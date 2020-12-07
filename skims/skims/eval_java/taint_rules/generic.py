# Local libraries
from eval_java.model import (
    StatementAdd,
    StatementAssignment,
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
    class_instantiation,
    declaration,
    literal,
    lookup,
    primary,
)


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False

        if isinstance(statement, StatementAdd):
            add.taint(statements, index)
        elif isinstance(statement, StatementAssignment):
            assignment.taint(statements, index)
        elif isinstance(statement, StatementCustomMethodInvocation):
            call.taint(statements, index)
        elif isinstance(statement, StatementClassInstantiation):
            class_instantiation.taint(statements, index)
        elif isinstance(statement, StatementDeclaration):
            declaration.taint(statements, index)
        elif isinstance(statement, StatementLiteral):
            literal.taint(statement)
        elif isinstance(statement, StatementLookup):
            lookup.taint(statements, index)
        elif isinstance(statement, StatementPrimary):
            primary.taint(statements, index)
        else:
            raise NotImplementedError()
