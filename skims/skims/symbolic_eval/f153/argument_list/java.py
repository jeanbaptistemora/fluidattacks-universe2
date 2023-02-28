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
    if (
        (len(child_args) == 2)
        and (header_name := nodes[child_args[0]].get("value"))
        and (header_val := nodes[child_args[1]].get("value"))
        and (header_name[1:-1] == "Accept")
        and (header_val[1:-1] == "*/*")
    ):
        args.triggers.add("all_myme_types_allowed")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
