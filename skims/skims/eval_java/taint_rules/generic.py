# Local libraries
from eval_java.model import (
    StatementAdd,
    StatementClassInstantiation,
    StatementCustomMethodInvocation,
    StatementDeclaration,
    StatementLiteral,
    StatementLookup,
    Statements,
)
from eval_java.taint_rules import (
    add,
    call,
    class_instantiation,
    declaration,
    literal,
    lookup,
)


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False

        if isinstance(statement, StatementAdd):
            add.taint(statements, index)
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
        else:
            raise NotImplementedError()
