from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def unsafe_sql_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["expression"].split(".")[-1] == "createConnection":
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
