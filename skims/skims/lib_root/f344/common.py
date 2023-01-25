from lib_root.utilities.javascript import (
    get_default_alias,
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
    Dict,
    Optional,
    Set,
)
from utils import (
    graph as g,
)


def get_local_storage_values_n_ids(graph: Graph) -> Set[NId]:
    n_ids: Set[NId] = set()
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


def local_storage_from_http(graph: Graph, method: MethodsEnum) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in get_local_storage_values_n_ids(graph):
        if is_vuln(graph, method, n_id):
            vuln_nodes.add(n_id)

    for n_id in g.matching_nodes(graph, label_type="Assignment"):
        vuln_nodes.update(is_vuln_assignment(graph, method, n_id))
    return vuln_nodes


def get_suspicious_names(graph: Graph) -> Dict[str, Set[NId]]:
    susp_names: Dict[str, Set[NId]] = {}
    for n_id in get_local_storage_values_n_ids(graph):
        if (graph.nodes[n_id].get("label_type") == "SymbolLookup") and (
            symbol := graph.nodes[n_id].get("symbol")
        ):
            if susp_names.get(symbol):
                susp_names[symbol].add(n_id)
            else:
                susp_names[symbol] = {n_id}

        if (graph.nodes[n_id].get("label_type") == "MemberAccess") and (
            member := graph.nodes[n_id].get("member")
        ):
            if susp_names.get(member):
                susp_names[member].add(n_id)
            else:
                susp_names[member] = {n_id}
    return susp_names


def get_async_danger_imports(graph: Graph) -> Set[str]:
    danger_imports: Set[str] = {"fetch"}
    if axios_alias := get_default_alias(graph, "axios"):
        danger_imports.add(axios_alias)
    if ky_alias := get_default_alias(graph, "ky"):
        danger_imports.add(ky_alias)
    if ky_universal_alias := get_default_alias(graph, "ky-universal"):
        danger_imports.add(ky_universal_alias)
    return danger_imports


def get_danger_expression(graph: Graph, n_id: NId) -> Optional[str]:
    if (
        (
            value_nodes := g.get_nodes_by_path(
                graph, n_id, [], "AwaitExpression", "MethodInvocation"
            )
        )
        and (val_n_id := value_nodes[0])
        and (whole_exp := graph.nodes[val_n_id].get("expression"))
        and (exp := whole_exp.split(".")[0])
    ):
        return exp
    return None


def local_storage_from_async(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    dangerous_imports: Set[str] = get_async_danger_imports(graph)
    suspicious_names: Dict[str, Set[NId]] = get_suspicious_names(graph)

    for n_id in g.matching_nodes(graph, label_type="VariableDeclaration"):
        if (
            (var_name := graph.nodes[n_id].get("variable"))
            and suspicious_names.get(var_name)
            and (exp := get_danger_expression(graph, n_id))
            and exp in dangerous_imports
        ):
            vuln_nodes.update(suspicious_names[var_name])
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
