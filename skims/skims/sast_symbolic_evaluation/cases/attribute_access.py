from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    (parent,) = args.dependencies
    args.syntax_step.meta.danger = parent.meta.danger
