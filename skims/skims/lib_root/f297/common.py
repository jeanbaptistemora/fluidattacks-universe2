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
from utils.string import (
    split_on_last_dot,
)


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> list[str]:
    vuln_nodes: list[str] = []
    for nid in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name: tuple[str, str] = split_on_last_dot(
            graph.nodes[nid]["expression"]
        )
        if f_name[-1] == "query" and is_argument_vuln(graph, nid, method):
            vuln_nodes.append(nid)

    return vuln_nodes


def is_argument_vuln(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
) -> bool:
    danger = {"UserConnection", "NonParametrizedQuery"}

    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger:
            return True
    return False
