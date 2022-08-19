from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id].get("name") == "Regex" and (
        args_nid := g.get_ast_childs(args.graph, args.n_id, "ArgumentList")
    ):
        args_ids = g.adj_ast(args.graph, args_nid[0])
        d_argument1 = args.generic(args.fork_n_id(args_ids[0])).danger
        if d_argument1:
            args.triggers.add("DangerousRegex")
        d_argument2 = True
        if len(args_ids) == 3:
            d_argument2 = args.generic(args.fork_n_id(args_ids[2])).danger
        args.evaluation[args.n_id] = d_argument1 and d_argument2

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
