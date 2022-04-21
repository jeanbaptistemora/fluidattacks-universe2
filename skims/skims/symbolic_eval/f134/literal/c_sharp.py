from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    if args.graph.nodes[args.n_id]["value"] == '"*"':
        args.evaluation[args.n_id] = True

    return args.evaluation[args.n_id]
