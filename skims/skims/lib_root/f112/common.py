from lib_root.utilities.javascript import (
    file_imports_module,
)
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
    Set,
)
from utils import (
    graph as g,
)


def get_eval_danger(
    graph: Graph, n_id: NId, danger_set: Set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def has_create_pool(graph: Graph) -> bool:
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        m_name = graph.nodes[n_id]["expression"].split(".")
        if m_name[-1] in {"createPool", "createPoolCluster"}:
            return True
    return False


def sql_injection(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_set = {"userconnection"}

    if not file_imports_module(graph, "mysql"):
        return vuln_nodes

    if has_create_pool(graph):
        danger_set = set()

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        n_attrs = graph.nodes[n_id]
        expr = n_attrs["expression"].split(".")
        if (
            expr[-1] == "query"
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args_ids := g.adj_ast(graph, al_id))
            and len(args_ids) >= 1
            and get_eval_danger(graph, n_id, danger_set, method)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
