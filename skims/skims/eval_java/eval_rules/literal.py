# Local libraries
from eval_java.model import (
    Statements,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    if statement.value_type == 'number':
        statement.meta.value = float(statement.value)

    # A literal is constant, no danger there
    statement.meta.danger = False
