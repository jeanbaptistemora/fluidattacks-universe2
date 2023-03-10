from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def weak_random(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        if (
            "cookie" in graph.nodes[n_id]["expression"]
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_nid := g.match_ast(graph, al_id).get("__1__"))
            and get_node_evaluation_results(
                method, graph, test_nid, {"Random"}, False
            )
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
