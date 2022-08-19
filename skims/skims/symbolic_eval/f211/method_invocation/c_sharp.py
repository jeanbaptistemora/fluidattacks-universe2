from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def is_regex_danger(args: SymbolicEvalArgs, expr: str) -> bool:
    regex_node = None
    if regex_name := expr.split(".")[0]:
        for vid in g.filter_nodes(
            args.graph,
            nodes=args.graph.nodes,
            predicate=g.pred_has_labels(label_type="VariableDeclaration"),
        ):
            if args.graph.nodes[vid].get("variable") == regex_name:
                regex_node = vid
                break
    if regex_node:
        return args.generic(args.fork_n_id(regex_node)).danger
    return False


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    method_n = args.graph.nodes[args.n_id]
    expr = method_n.get("expression")

    if "TimeSpan" in expr:
        args.triggers.add("Timespan")
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    if expr.split(".")[1] == "Escape":
        args.triggers.add("Escaped")
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    args_id = g.get_ast_childs(args.graph, args.n_id, "ArgumentList", depth=1)
    args_nid = g.adj_ast(args.graph, args_id[0], depth=1)

    d_argument1 = False
    if len(args_nid) == 1:
        d_argument1 = True
    elif len(args_nid) >= 2:
        d_argument1 = args.generic(args.fork_n_id(args_nid[1])).danger

    if d_argument1:
        args.triggers.add("DangerousRegex")

    if len(args_nid) == 4:
        args.generic(args.fork_n_id(args_nid[3]))

    d_argument2 = is_regex_danger(args, expr)

    args.evaluation[args.n_id] = d_argument1 and d_argument2

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
