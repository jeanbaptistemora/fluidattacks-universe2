# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze the arguments involved in the addition
    left = common.read_stack(statements, index)
    right = common.read_stack(statements, index)
    left_danger = any(arg.meta.danger for arg in left)
    right_danger = any(arg.meta.danger for arg in right)

    # Local context
    statement.meta.danger = left_danger or right_danger
