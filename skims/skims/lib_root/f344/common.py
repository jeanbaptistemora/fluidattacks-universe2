from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from networkx.classes.reportviews import (
    NodeView,
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


def get_local_storage_values_n_ids(graph: Graph) -> set[NId]:
    n_ids: set[NId] = set()
    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="localStorage.setItem"
    ):
        if (
            parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList")
        ) and (value_n_id := g.adj(graph, parameters_n_id)[1]):
            n_ids.add(value_n_id)
    return n_ids


def is_vuln(graph: Graph, method: MethodsEnum, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.danger:
            return True
    return False


def local_storage_from_http(graph: Graph, method: MethodsEnum) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for n_id in get_local_storage_values_n_ids(graph):
        if is_vuln(graph, method, n_id):
            vuln_nodes.add(n_id)
    return vuln_nodes


def get_assignment_values_n_ids(graph: Graph) -> set[NId]:
    n_ids: set[NId] = set()
    nodes: NodeView = graph.nodes
    for n_id in g.matching_nodes(graph, label_type="Assignment"):
        if (
            (var_n_id := nodes[n_id].get("variable_id"))
            and (nodes[var_n_id].get("label_type") == "MemberAccess")
            and (nodes[var_n_id].get("member") == "client")
            and (nodes[var_n_id].get("expression") == "onload")
        ):
            n_ids.add(nodes[n_id].get("value_id"))
    return n_ids


def vuln_assignment_n_ids(
    graph: Graph, method: MethodsEnum, n_id: NId
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            vuln_n_ids = set(
                map(lambda x: x.split("this_")[1], evaluation.triggers)
            )
            vuln_nodes.update(vuln_n_ids)
    return vuln_nodes


def local_storage_from_assignment(
    graph: Graph, method: MethodsEnum
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for n_id in get_assignment_values_n_ids(graph):
        vuln_n_ids = vuln_assignment_n_ids(graph, method, n_id)
        vuln_nodes.update(vuln_n_ids)
    return vuln_nodes
