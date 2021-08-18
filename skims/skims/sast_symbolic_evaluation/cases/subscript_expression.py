from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    StopEvaluation,
)


def evaluate(args: EvaluatorArgs) -> None:
    if len(args.dependencies) != 2:
        raise StopEvaluation.from_args(args)

    _, _object = args.dependencies
    args.syntax_step.meta.value = args.dependencies[1].meta.value
    args.syntax_step.meta.danger = _object.meta.danger
