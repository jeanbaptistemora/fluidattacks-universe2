# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
    lookup_var_state_by_name,
)
from utils.string import (
    split_on_last_dot,
)


def evaluate(args: EvaluatorArgs) -> None:
    if '.' in args.syntax_step.symbol:
        var_name, field = split_on_last_dot(args.syntax_step.symbol)
        if args.current_instance and (
                field_instance := args.current_instance.fields.get(field)):
            args.syntax_step.meta.danger = field_instance.meta.danger
            args.syntax_step.meta.value = field_instance.meta.value
        elif var_decl := lookup_var_dcl_by_name(args, var_name):
            args.syntax_step.meta.danger = var_decl.meta.danger
            args.syntax_step.meta.value = var_decl.meta.value
        return None

    if dcl := lookup_var_state_by_name(args, args.syntax_step.symbol):
        # Found it!
        args.syntax_step.meta.danger = dcl.meta.danger
        args.syntax_step.meta.value = dcl.meta.value

    return None
