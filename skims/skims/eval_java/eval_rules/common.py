# Local libraries
from eval_java.model import (
    StatementAssignment,
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
    return list(reversed(tuple(
        statement
        for statement in statements[0:index]
        if isinstance(statement, (
            StatementAssignment,
            StatementDeclaration,
        ))
    )))


def read_stack_var_type(
    statements: Statements,
    index: int,
    var: str,
) -> str:
    for symbol in read_stack_symbols(statements, index):
        if symbol.var == var and isinstance(symbol, StatementDeclaration):
            return symbol.var_type

    return ''
