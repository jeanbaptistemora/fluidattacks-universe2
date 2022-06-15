from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = (
        ma_attr["expression"] == "Diagnostics.Process"
        and ma_attr["member"] == "Start"
    ) or ma_attr["member"] == "Execute"
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
