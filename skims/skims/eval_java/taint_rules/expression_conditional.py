# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze the arguments involved in the expression
    _, true, false = common.read_stack(statements, index)

    # Local context
    statement.meta.danger = true.meta.danger or false.meta.danger
