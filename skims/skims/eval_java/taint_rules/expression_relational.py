# Standard library
import contextlib

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
    left, right = common.read_stack(statements, index)

    with contextlib.suppress(TypeError):
        if statement.operator == '>':
            statement.meta.value = left.meta.value > right.meta.value
        elif statement.operator == '>=':
            statement.meta.value = left.meta.value >= right.meta.value
        elif statement.operator == '<':
            statement.meta.value = left.meta.value < right.meta.value
        elif statement.operator == '<=':
            statement.meta.value = left.meta.value <= right.meta.value

    # This kind of node just affects control flow
    statement.meta.danger = False
