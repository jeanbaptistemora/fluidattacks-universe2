# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = args.dependencies[0].meta.danger
