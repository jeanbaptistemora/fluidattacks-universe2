from model.core_model import (
    MethodsEnum,
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


def is_salt_harcoded(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def has_dangerous_param(graph: Graph, method: MethodsEnum) -> list[NId]:
    sensitive_methods = {"salt", "SALT"}

    return [
        n_id
        for n_id in g.matching_nodes(graph, label_type="SymbolLookup")
        if graph.nodes[n_id].get("symbol") in sensitive_methods
        and is_salt_harcoded(graph, n_id, method)
    ]
