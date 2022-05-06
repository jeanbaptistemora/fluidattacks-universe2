from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"] == '"true"':
        args.evaluation[args.n_id] = True
        args.triggers.add('"true"')

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
