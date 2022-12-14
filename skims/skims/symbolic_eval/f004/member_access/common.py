from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if f'{n_attrs["member"]}.{n_attrs["expression"]}' in {
        "req.query",
        "req.params",
        "req.body",
    }:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
