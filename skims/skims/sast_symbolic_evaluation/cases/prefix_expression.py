from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    [expression] = args.dependencies
    args.syntax_step.meta.danger = expression.meta.danger
