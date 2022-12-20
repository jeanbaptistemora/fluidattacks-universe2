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
from typing import (
    List,
)
from utils import (
    graph as g,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.triggers == {"Random"}:
            return True
    return False


def weak_random(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.matching_nodes(
        graph,
        label_type="MethodInvocation",
    ):
        if (
            "cookie" in graph.nodes[n_id]["expression"]
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, al_id).get("__1__"))
            and get_eval_danger(graph, test_node, method)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
