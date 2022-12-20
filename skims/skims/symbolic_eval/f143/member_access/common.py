from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def is_user_input(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_js_ts_http_inputs(args):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
