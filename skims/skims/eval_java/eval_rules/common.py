# Standard library
from typing import (
    Optional,
)

# Local libraries
from eval_java.model import (
    Statement,
    StatementAssignment,
    StatementDeclaration,
    Statements,
)


def read_stack(
    statements: Statements,
    index: int,
) -> Statements:
    stacks: Statements = []
    stacks_expected_length: int = -statements[index].meta.stack

    stack_depth: int = 0

    while len(stacks) < stacks_expected_length:
        index -= 1

        if stack_depth:
            stack_depth += 1
        else:
            stacks.append(statements[index])

        stack_depth += statements[index].meta.stack

    return list(reversed(stacks))


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


def read_stack_var(
    statements: Statements,
    index: int,
    var: str,
) -> Optional[Statement]:
    for symbol in read_stack_symbols(statements, index):
        if symbol.var == var:
            return symbol

    return None


def read_stack_var_type(
    statements: Statements,
    index: int,
    var: str,
) -> str:
    for symbol in read_stack_symbols(statements, index):
        if symbol.var == var and isinstance(symbol, StatementDeclaration):
            return symbol.var_type

    return ''
