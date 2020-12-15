# Local libraries
from eval_java.model import (
    Statements,
)


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]
    statement.meta.danger = False
