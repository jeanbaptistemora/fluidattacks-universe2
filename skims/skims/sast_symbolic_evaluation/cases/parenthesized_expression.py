# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(
        dep.meta.danger for dep in args.dependencies
    )
    if len(args.dependencies) == 1:
        args.syntax_step.meta.value = args.dependencies[0].meta.value
