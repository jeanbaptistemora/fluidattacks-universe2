# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    if args.syntax_step.value_type in {
        "boolean",
        "null",
    }:
        args.syntax_step.meta.value = {
            "false": False,
            "null": None,
            "true": True,
        }[args.syntax_step.value]
    elif args.syntax_step.value_type == "number":
        args.syntax_step.meta.value = float(args.syntax_step.value)
    elif args.syntax_step.value_type == "string":
        args.syntax_step.meta.value = args.syntax_step.value
    else:
        raise NotImplementedError()
