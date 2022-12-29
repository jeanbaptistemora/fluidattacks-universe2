from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_sql_float(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "*http.Request":
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
