from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
    string,
)


def java_sql_injection(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    lib = string.build_attr_paths(
        "javax", "servlet", "http", "HttpServletRequest"
    )

    if args.graph.nodes[args.n_id]["variable_type"] in lib:
        args.triggers.add("userconnection")
    elif (
        (mod_id := g.match_ast_d(args.graph, args.n_id, "Modifiers"))
        and (annot_id := g.match_ast_d(args.graph, mod_id, "Annotation"))
        and args.graph.nodes[annot_id].get("name") == "RequestParam"
    ):
        args.evaluation[args.n_id] = True
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
