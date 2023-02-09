from model.graph_model import (
    Graph,
    NAttrs,
    NAttrsPredicateFunction,
    NId,
)
from typing import (
    Iterable,
    List,
    Tuple,
)
from utils import (
    graph as g,
)


def has_labels(n_attrs: NAttrs, value: str) -> bool:

    vals = list(n_attrs.values())
    for val in vals:
        if value in str(val):
            return True
    return False


def pred_has_labels(value: str) -> NAttrsPredicateFunction:
    def predicate(n_attrs: NAttrs) -> bool:
        return has_labels(n_attrs, value)

    return predicate


def filter_nodes(
    graph: Graph,
    nodes: Iterable[str],
    predicate: NAttrsPredicateFunction,
) -> Tuple[str, ...]:
    bad_labels = ["comment", "string"]
    result: Tuple[str, ...] = tuple(
        n_id
        for n_id in nodes
        if predicate(graph.nodes[n_id])
        and graph.nodes[n_id]["label_type"] not in bad_labels
    )
    return result


def matching_nodes_custom(graph: Graph, value: str) -> Tuple[str, ...]:
    return filter_nodes(graph, graph.nodes, pred_has_labels(value))


def is_import_used(
    graph: Graph,
    identifier: str,
) -> bool:
    if identifier == "React":
        return True
    vuln_nodes: List[NId] = []

    for nid_tuple in matching_nodes_custom(graph, value=identifier):
        vuln_nodes.append(nid_tuple)
    if len(vuln_nodes) > 1:
        return True
    return False


def simple_import(
    graph: Graph, identifier_nodes: Tuple[NId, ...]
) -> List[NId]:
    vuln_nodes: List[NId] = []
    for nid in identifier_nodes:
        name = graph.nodes[nid]["label_text"]
        if not is_import_used(graph, name):
            vuln_nodes.append(nid)
    return vuln_nodes


def named_imports(graph: Graph, specifier_nodes: Tuple[NId, ...]) -> List[NId]:
    vuln_nodes: List[NId] = []
    for nid in specifier_nodes:
        if alias := graph.nodes[nid].get("label_field_alias"):
            identifier = graph.nodes[alias]["label_text"]
        else:
            name = graph.nodes[nid]["label_field_name"]
            identifier = graph.nodes[name]["label_text"]
        if not is_import_used(graph, identifier):
            vuln_nodes.append(nid)
    return vuln_nodes


def import_is_not_used(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.matching_nodes(graph, label_type="import_clause"):
        specifier = g.get_ast_childs(
            graph, n_id, depth=2, label_type="import_specifier"
        )
        identifier = g.get_ast_childs(graph, n_id, label_type="identifier")

        if identifier:
            vuln_nodes += simple_import(graph, identifier)
        if specifier:
            vuln_nodes += named_imports(graph, specifier)
    return vuln_nodes
