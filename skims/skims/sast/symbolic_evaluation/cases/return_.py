# Local libraries
from sast.symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    returned, = args.dependencies
    args.syntax_step.meta.danger = returned.meta.danger
    args.syntax_step.meta.value = returned.meta.value
