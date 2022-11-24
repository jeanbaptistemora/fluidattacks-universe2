from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_authentication(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "HttpHeaders":
        args.evaluation[args.n_id] = True
        args.triggers.add("ObjectCreation")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
