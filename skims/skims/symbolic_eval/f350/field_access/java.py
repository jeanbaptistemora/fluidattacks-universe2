from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_ACCESS = {
    "insecuretrustmanagerfactory.instance",
}


def java_insecure_trust_manager(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["field_text"].lower() in DANGER_ACCESS:
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
