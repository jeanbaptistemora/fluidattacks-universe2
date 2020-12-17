# Third party libraries
import contextlib

# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    common,
)


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze the arguments involved in the addition
    right, left = common.read_stack(statements, index)

    # Propagate values if possible
    with contextlib.suppress(TypeError):
        if statement.sign == '+':
            statement.meta.value = left.meta.value + right.meta.value
        elif statement.sign == '-':
            statement.meta.value = left.meta.value - right.meta.value
        else:
            raise NotImplementedError()

    # Local context
    statement.meta.danger = left.meta.danger or right.meta.danger
