from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_cookie(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if args.graph.nodes[key]["symbol"] == "secure":
        val_danger = args.generic(args.fork(n_id=value)).danger
        if val_danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("InsecureCookie")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
