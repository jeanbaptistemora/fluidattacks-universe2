# Local libraries
from eval_java.model import (
    Statements,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]
    statement.meta.danger = False
