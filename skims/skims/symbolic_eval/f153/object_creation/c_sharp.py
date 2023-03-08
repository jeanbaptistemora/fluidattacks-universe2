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

    if (
        nodes[args.n_id].get("name") == "MediaTypeWithQualityHeaderValue"
        and (args_id := nodes[args.n_id].get("arguments_id"))
        and (arguments := g.adj_ast(args.graph, args_id))
    ):
        for arg in arguments:
            if (
                nodes[arg].get("label_type") == "Literal"
                and (val := nodes[arg].get("value"))
                and val[1:-1] == "*/*"
            ):
                args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
