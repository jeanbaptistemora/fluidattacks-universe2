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
    Set,
)
from utils import (
    graph as g,
)


def is_vuln(graph: Graph, method: MethodsEnum, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.danger:
            return True
    return False


def local_storage_from_http(graph: Graph, method: MethodsEnum) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="localStorage.setItem"
    ):
        if (
            (parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList"))
            and (value_n_id := g.adj(graph, parameters_n_id)[1])
            and is_vuln(graph, method, value_n_id)
        ):
            vuln_nodes.add(n_id)
    return vuln_nodes
