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


def is_smell_dangerous(values: Set[str]) -> bool:
    conditions = {
        "auth",
        "credential",
        "documentousuario",
        "jwt",
        "password",
        "sesiondata",
        "sesionid",
        "sesiontoken",
        "sessiondata",
        "sessionid",
        "sessiontoken",
        "tokenaccess",
        "tokenapp",
        "tokenid",
        "nameuser",
        "nombreusuario",
        "mailuser",
    }

    item = re.sub("[^A-Za-z0-9]+", "", "".join(values)).lower()
    if item in conditions and not could_be_boolean(item):
        return True
    return False


def is_insecure_storage(graph: Graph, nid: NId, method: MethodsEnum) -> bool:
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
        if evaluation:
            return is_smell_dangerous(evaluation.triggers)

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
