from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
    pred_ast,
)


def kt_insecure_certification(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    parent = pred_ast(graph, args.n_id)

    if (
        parent
        and (graph.nodes[parent[0]]["expression"]).split(".")[1] == "init"
    ):
        c_ids = adj_ast(graph, args.n_id)
        check_client_trusted = graph.nodes[c_ids[1]]["label_type"]
        if check_client_trusted == "SymbolLookup":
            args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
