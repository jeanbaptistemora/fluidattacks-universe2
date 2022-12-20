from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
import re
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    List,
    Set,
    Tuple,
)
from utils import (
    graph as g,
)


def could_be_boolean(key: str) -> bool:
    prefixes = {"is", "has", "es"}
    match = re.search("[a-z]", key, re.I)
    if match:
        _key = key[match.start() :]
        return any(_key.startswith(prefix) for prefix in prefixes)
    return False


def is_insecure_storage(graph: Graph, nid: NId, method: MethodsEnum) -> bool:
    conditions: Tuple[Set[str], ...] = (
        # All items in the set must be present to consider it sensitive info
        {"auth"},
        {"credential"},
        {"documento", "usuario"},
        {"jwt"},
        {"password"},
        {"sesion", "data"},
        {"sesion", "id"},
        {"sesion", "token"},
        {"session", "data"},
        {"session", "id"},
        {"session", "token"},
        {"token", "access"},
        {"token", "app"},
        {"token", "id"},
        {"name", "user"},
        {"nombre", "usuario"},
        {"mail", "user"},
    )
    f_name = graph.nodes[nid]["expression"]

    al_id = graph.nodes[nid].get("arguments_id")
    if not al_id:
        return False
    opc_nid = g.match_ast(graph, al_id)

    if "getItem" in f_name.split("."):
        test_node = opc_nid.get("__0__")
    else:
        test_node = opc_nid.get("__1__")

    if not test_node:
        return False

    for path in get_backward_paths(graph, test_node):
        evaluation = evaluate(method, graph, path, test_node)
        if evaluation and any(
            all(smell in key_str.lower() for smell in smells)
            and not could_be_boolean(key_str.lower())
            for key_str in evaluation.triggers
            for smells in conditions
        ):
            return True

    return False


def client_storage(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_names = {
        "localStorage.getItem",
        "localStorage.setItem",
        "sessionStorage.getItem",
        "sessionStorage.setItem",
    }
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        if f_name in danger_names and is_insecure_storage(graph, n_id, method):
            vuln_nodes.append(n_id)
    return vuln_nodes
