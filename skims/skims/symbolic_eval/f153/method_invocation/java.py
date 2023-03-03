from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def allow_all_mime_types(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    node = args.graph.nodes[args.n_id]

    dang_expressions = {"Builder", "newBuilder"}
    dang_classes = {"HttpRequest"}

    if (
        node.get("expression") in dang_expressions
        and (object_id := node.get("object_id"))
        and nodes[object_id].get("symbol") in dang_classes
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
