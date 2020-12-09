# Local libraries
from eval_java.model import (
    Statements,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # A literal is constant, no danger there
    statement.meta.danger = False
