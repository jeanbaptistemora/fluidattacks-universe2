from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_trust_manager(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if (
        args.graph.nodes[args.n_id]["symbol"].lower()
        == "insecuretrustmanagerfactory.instance"
    ):
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
