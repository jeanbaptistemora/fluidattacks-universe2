# Local libraries
from sast.symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast.symbolic_evaluation.utils.generic import (
    lookup_var_state_by_name,
)


def evaluate(args: EvaluatorArgs) -> None:
    if dcl := lookup_var_state_by_name(args, args.syntax_step.symbol):
        # Found it!
        args.syntax_step.meta.danger = dcl.meta.danger
        args.syntax_step.meta.value = dcl.meta.value
