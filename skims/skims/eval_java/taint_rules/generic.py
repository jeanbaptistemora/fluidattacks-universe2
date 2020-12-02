# Local libraries
from eval_java.model import (
    StatementAdd,
    StatementBinding,
    StatementClassInstantiation,
    StatementCustomMethodInvocation,
    StatementLiteral,
    StatementLookup,
    Statements,
)
from eval_java.taint_rules import (
    add,
    binding,
    call,
    class_instantiation,
    literal,
    lookup,
)


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement.meta.danger = False

        if isinstance(statement, StatementAdd):
            add.taint(statements, index)
        elif isinstance(statement, StatementBinding):
            binding.taint(statements, index)
        elif isinstance(statement, StatementCustomMethodInvocation):
            call.taint(statements, index)
        elif isinstance(statement, StatementClassInstantiation):
            class_instantiation.taint(statements, index)
        elif isinstance(statement, StatementLiteral):
            literal.taint(statement)
        elif isinstance(statement, StatementLookup):
            lookup.taint(statements, index)
        else:
            raise NotImplementedError()
