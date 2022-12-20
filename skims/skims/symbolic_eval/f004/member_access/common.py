from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_js_ts_http_inputs(args):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
