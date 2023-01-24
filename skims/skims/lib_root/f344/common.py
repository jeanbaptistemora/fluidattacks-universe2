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


def is_vuln_assignment(
    graph: Graph, method: MethodsEnum, n_id: NId
) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for path in get_backward_paths(graph, n_id):
        if (
            (evaluation := evaluate(method, graph, path, n_id))
            and ("xml_instance" in evaluation.triggers)
            and ("onload" in evaluation.triggers)
        ):
            evaluation.triggers.difference_update({"xml_instance", "onload"})
            vuln_nodes.update(evaluation.triggers)
    return vuln_nodes


def ls_direct_usage(graph: Graph, method: MethodsEnum) -> Set[NId]:
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


def xml_onload_assignment(graph: Graph, method: MethodsEnum) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in g.matching_nodes(graph, label_type="Assignment"):
        vuln_nodes.update(is_vuln_assignment(graph, method, n_id))
    return vuln_nodes


def local_storage_from_http(graph: Graph, method: MethodsEnum) -> Set[NId]:

    vuln_nodes: Set[NId] = set()
    vuln_nodes.update(ls_direct_usage(graph, method))
    vuln_nodes.update(xml_onload_assignment(graph, method))

    return vuln_nodes


def local_storage_from_callback(graph: Graph, method: MethodsEnum) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in g.matching_nodes(
        graph, label_type="Placeholder", expression="PlaceHolder"
    ):
        if (
            (parameters_n_id := g.match_ast_d(graph, n_id, "PlaceHolder"))
            and (value_n_id := g.adj(graph, parameters_n_id)[1])
            and is_vuln(graph, method, value_n_id)
        ):
            vuln_nodes.add(n_id)
    return vuln_nodes
