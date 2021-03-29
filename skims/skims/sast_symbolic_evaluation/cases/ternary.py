# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    predicate, left, right = args.dependencies

    if predicate.meta.value is True:
        args.syntax_step.meta.danger = left.meta.danger
        args.syntax_step.meta.value = left.meta.value
    elif predicate.meta.value is False:
        args.syntax_step.meta.danger = right.meta.danger
        args.syntax_step.meta.value = right.meta.value
    elif predicate.meta.value is None:
        args.syntax_step.meta.danger = left.meta.danger or right.meta.danger
    else:
        raise NotImplementedError(predicate.meta.value)
