from symbolic_eval.common import (
    check_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = check_http_inputs(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
