from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

SAFE_METHODS = {"sanitizeHtml"}


def common_reflected_xss(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["expression"] in SAFE_METHODS:
        args.triggers.add("SafeValidation")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
