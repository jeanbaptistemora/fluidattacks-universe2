from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)


def is_insecure_header(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def insecure_cookies(graph: Graph, method: MethodsEnum) -> List[str]:
    vuln_nodes: List[str] = []
    danger_methods = {"cookieService"}
    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        expression = graph.nodes[n_id].get("expression")
        exprlit = expression.split(".")
        print(exprlit)
        if any(
            exp in exprlit for exp in danger_methods
        ) and is_insecure_header(graph, n_id, method):
            vuln_nodes.append(n_id)

    return vuln_nodes
