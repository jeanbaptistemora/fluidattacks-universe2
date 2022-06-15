from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_info_leak_errors(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"] == '"true"':
        args.evaluation[args.n_id] = True
        args.triggers.add('"true"')

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
