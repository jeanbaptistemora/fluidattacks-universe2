from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def common_sql_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    if args.graph.nodes[args.n_id]["member"] == "req.query":
        args.triggers.add("UserConnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
