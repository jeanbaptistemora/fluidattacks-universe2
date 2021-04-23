# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    (src,) = args.dependencies

    args.syntax_step.meta.danger = src.meta.danger
