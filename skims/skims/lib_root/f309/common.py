from collections.abc import (
    Set,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def get_eval_danger(
    graph: Graph,
    n_id: NId,
    rules: Set[str],
    method: core_model.MethodsEnum,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def is_insecure_jwt(
    graph: Graph,
    n_id: NId,
    method: core_model.MethodsEnum,
) -> bool:
    rules = {"unsafealgorithm"}
    member = graph.nodes[n_id].get("member")

    parent = g.pred(graph, n_id)[0]
    al_id = graph.nodes[parent].get("arguments_id")
    if not al_id:
        return False

    args_ids = g.adj_ast(graph, al_id)
    if len(args_ids) > 2:
        return get_eval_danger(graph, args_ids[2], rules, method)

    if member == "jwt" and len(args_ids) <= 2:
        return True

    return False
