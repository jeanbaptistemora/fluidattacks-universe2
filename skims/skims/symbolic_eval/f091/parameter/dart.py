from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def dart_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
