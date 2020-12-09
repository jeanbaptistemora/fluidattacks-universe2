# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze if the arguments involved in the cast are dangerous
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Local context
    statement.meta.danger = args_danger
