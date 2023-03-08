from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kt_insecure_cert(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "X509TrustManager":
        args.triggers.add("TrustManager")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
