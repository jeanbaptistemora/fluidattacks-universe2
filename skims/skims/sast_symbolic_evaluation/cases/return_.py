from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    # Propagate danger and value when only returning one value
    if len(args.dependencies) == 1:
        (returned,) = args.dependencies
        args.syntax_step.meta.danger = returned.meta.danger
        args.syntax_step.meta.value = returned.meta.value
    # For the time being, only propagate danger if there are multiple return
    # values
    else:
        args.syntax_step.meta.danger = any(
            dep.meta.danger for dep in args.dependencies
        )
