from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_sql_user_params(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "SqlParameter":
        args.triggers.add("SantitizedParameter")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
