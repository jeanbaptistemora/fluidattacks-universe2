from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def common_regex_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    if check_js_ts_http_inputs(args):
        args.triggers.add("UserConnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
