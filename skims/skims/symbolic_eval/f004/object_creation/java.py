from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_OBJECTS = {
    "SeparateClassRequest",
}


def java_remote_command_execution(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if any(danger_obj in ma_attr["name"] for danger_obj in DANGER_OBJECTS):
        args.triggers.add("UserParams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
