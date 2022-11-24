from model.core_model import (
    FindingEnum,
)
from sast_symbolic_evaluation.decorators import (
    javascript_only,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    StopEvaluation,
)
from utils.languages.javascript import (
    is_cipher_vulnerable as javascript_cipher_is_vulnerable,
)


@javascript_only
def danger_literals(args: EvaluatorArgs) -> None:
    if (
        args.finding == FindingEnum.F052
        and args.syntax_step.value_type == "string"
    ):
        args.syntax_step.meta.danger = javascript_cipher_is_vulnerable(
            args.syntax_step.value
        )


def evaluate(args: EvaluatorArgs) -> None:
    if args.syntax_step.value_type in {
        "boolean",
        "null",
    }:
        args.syntax_step.meta.value = {
            "false": False,
            "nil": None,
            "null": None,
            "true": True,
            "undefined": None,
        }[args.syntax_step.value]
    elif args.syntax_step.value_type == "number":
        args.syntax_step.meta.value = float(args.syntax_step.value)
    elif args.syntax_step.value_type == "string":
        args.syntax_step.meta.value = args.syntax_step.value
    elif args.syntax_step.value_type.startswith("struct["):
        args.syntax_step.meta.value = args.syntax_step.value
    else:
        raise StopEvaluation.from_args(args)

    danger_literals(args)
