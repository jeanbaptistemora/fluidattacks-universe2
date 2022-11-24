from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    (parent,) = args.dependencies
    attribute = args.syntax_step.attribute
    args.syntax_step.meta.danger = (
        parent.meta.value[attribute].danger
        if parent.meta.value and attribute in parent.meta.value
        else parent.meta.danger
    )
    args.syntax_step.meta.value = (
        parent.meta.value[attribute].value
        if parent.meta.value and attribute in parent.meta.value
        else parent.meta.value
    )
