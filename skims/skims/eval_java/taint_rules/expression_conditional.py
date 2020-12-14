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
    predicate, true, false = common.read_stack(statements, index)

    if predicate.meta.value is True:
        statement.meta.danger = true.meta.danger
    elif predicate.meta.value is False:
        statement.meta.danger = false.meta.danger
    else:
        statement.meta.danger = False
