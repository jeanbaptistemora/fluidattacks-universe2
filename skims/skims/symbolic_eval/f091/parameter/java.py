from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def java_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpServletRequest":
        args.evaluation[args.n_id] = True

    modifiers_id = g.match_ast_d(args.graph, args.n_id, "Modifiers")
    if modifiers_id:
        childs = g.adj_ast(args.graph, modifiers_id)
        if any(
            args.graph.nodes[_id].get("name") == "PathParam" for _id in childs
        ):
            args.evaluation[args.n_id] = True
            args.triggers.add("userparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
