# Local libraries
from eval_java.model import (
    Statement,
)


def taint(statement: Statement) -> None:
    # A literal is constant, no danger there
    statement['__danger__'] = False
