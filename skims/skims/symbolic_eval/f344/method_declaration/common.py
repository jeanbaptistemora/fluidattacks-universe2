from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def js_ls_sensitive_data(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if method_n_ids := g.match_ast_group(
        args.graph, args.n_id, "MethodInvocation", depth=-1
    )["MethodInvocation"]:
        for n_id in method_n_ids:
            node = args.graph.nodes[n_id]
            if node.get("expression") == "localStorage.setItem" and (
                (args_id := node.get("arguments_id"))
                and (arg_val := g.adj(args.graph, args_id)[1])
                and (args.graph.nodes[arg_val].get("member") == "this")
            ):
                args.triggers.add(arg_val)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
