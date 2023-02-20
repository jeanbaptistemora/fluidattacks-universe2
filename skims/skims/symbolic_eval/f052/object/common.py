from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def insecure_encrypt(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    obj_keys = []
    for pair_id in g.match_ast_group_d(args.graph, args.n_id, "Pair"):
        pair_node = args.graph.nodes[pair_id]
        key = pair_node["key_id"]
        obj_keys.append(args.graph.nodes[key]["symbol"])

    if not any(key == "mode" for key in obj_keys):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_sign(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    obj_keys = []
    for pair_id in g.match_ast_group_d(args.graph, args.n_id, "Pair"):
        pair_node = args.graph.nodes[pair_id]
        key = pair_node["key_id"]
        obj_keys.append(args.graph.nodes[key]["symbol"])

    if not any(key == "algorithm" for key in obj_keys):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
