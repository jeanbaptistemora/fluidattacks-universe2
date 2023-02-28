from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def allow_all_mime_types(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    nodes = args.graph.nodes
    danger_classes: set[str] = {"HttpURLConnection", "HttpRequest"}

    if (instance_class := nodes[args.n_id].get("variable_type")) and (
        instance_class in danger_classes
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
