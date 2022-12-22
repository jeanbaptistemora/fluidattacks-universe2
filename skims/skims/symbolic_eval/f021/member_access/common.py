from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def dynamic_xpath(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_js_ts_http_inputs(args):
        args.evaluation[args.n_id] = True
        args.triggers.add("userparameters")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
