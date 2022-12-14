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


def is_argument_vuln(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
) -> bool:
    danger = {"UserConnection"}

    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger:
            return True
    return False
