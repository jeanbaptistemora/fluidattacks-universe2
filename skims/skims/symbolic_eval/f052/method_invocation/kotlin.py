from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kt_insecure_cert(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    if graph.nodes[args.n_id]["expression"] == "SSLContext.getInstance":
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insec_key_gen(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    if graph.nodes[args.n_id]["expression"] == "KeyGenerator.getInstance":
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
