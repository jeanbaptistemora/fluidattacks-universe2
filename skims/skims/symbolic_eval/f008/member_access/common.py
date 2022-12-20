from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def unsafe_xss_content(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_js_ts_http_inputs(args):
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
