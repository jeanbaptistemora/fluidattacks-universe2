# Standard library
import operator
from contextlib import suppress

# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    left, right = args.dependencies

    args.syntax_step.meta.danger = left.meta.danger or right.meta.danger

    if left.meta.value is not None and right.meta.value is not None:
        with suppress(TypeError):
            args.syntax_step.meta.value = {
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.truediv,
                '<': operator.lt,
                '<=': operator.le,
                '==': operator.eq,
                '!=': operator.ne,
                '>': operator.gt,
                '>=': operator.ge,
            }.get(args.syntax_step.operator, lambda _, __: None)(
                left.meta.value,
                right.meta.value,
            )
