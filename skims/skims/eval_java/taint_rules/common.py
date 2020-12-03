# Local libraries
from eval_java.model import (
    StatementDeclaration,
    Statements,
)


def read_stack(
    statements: Statements,
    index: int,
) -> Statements:
    return statements[
        index + statements[index].meta.stack:
        index
    ]


def read_stack_symbols(
    statements: Statements,
    index: int,
) -> Statements:
    return [
        statement
        for statement in statements[0:index]
        if isinstance(statement, StatementDeclaration)
    ]
