from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def allow_all_mime_types(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    child_args = g.adj_ast(args.graph, args.n_id)

    if len(child_args) > 0 and len(child_args) % 2 == 0:
        for index in range(0, len(child_args), 2):
            if (nodes[child_args[index]].get("value")[1:-1] == "Accept") and (
                nodes[child_args[index + 1]].get("value")[1:-1] == "*/*"
            ):
                args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
