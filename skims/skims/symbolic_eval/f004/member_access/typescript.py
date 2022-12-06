from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def ts_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["member"] == "req.query":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
