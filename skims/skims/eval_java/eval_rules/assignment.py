# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    common,
)


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze the arguments involved in the assignment
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Local context
    statement.meta.danger = args_danger
