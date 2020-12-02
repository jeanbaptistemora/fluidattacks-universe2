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
    left = common.read_stack(statements, index, label='stack_0')
    right = common.read_stack(statements, index, label='stack_1')
    left_danger = any(arg['__danger__'] for arg in left)
    right_danger = any(arg['__danger__'] for arg in right)

    # Local context
    statement['__danger__'] = left_danger or right_danger
