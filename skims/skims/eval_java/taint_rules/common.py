# Local libraries
from eval_java.model import (
    Statements,
)


def read_stack(
    statements: Statements,
    index: int,
    *,
    label: str = 'stack'
) -> Statements:
    return statements[index + statements[index][label]:index]


def read_stack_symbols(
    statements: Statements,
    index: int,
) -> Statements:
    return [
        statement
        for statement in statements[0:index]
        if statement['type'] == 'BINDING'
    ]
