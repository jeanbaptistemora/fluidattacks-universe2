from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    (parent,) = args.dependencies
    args.syntax_step.meta.danger = parent.meta.danger
    args.syntax_step.meta.value = (
        parent.meta.value.get(args.syntax_step.attribute)
        if parent.meta.value
        else parent.meta.value
    )
