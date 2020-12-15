# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    common,
)


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]
    calls = common.read_stack(statements, index)
    # is vulnerable if any of the calls is
    statement.meta.danger = any(arg.meta.danger for arg in calls)
