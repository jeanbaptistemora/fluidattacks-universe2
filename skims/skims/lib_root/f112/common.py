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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def has_create_pool(graph: Graph) -> bool:
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        m_name = graph.nodes[n_id]["expression"].split(".")
        if m_name[-1] in {"createPool", "createPoolCluster"}:
            return True
    return False


def sql_injection(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
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
            and get_node_evaluation_results(method, graph, n_id, danger_set)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
