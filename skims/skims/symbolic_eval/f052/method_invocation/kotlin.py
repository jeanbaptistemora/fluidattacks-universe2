from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kt_insecure_certification(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    args.evaluation[args.n_id] = False
    if graph.nodes[args.n_id]["expression"] == "SSLContext.getInstance":
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
