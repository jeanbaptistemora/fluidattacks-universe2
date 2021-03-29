# Local libraries
from sast.symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False
