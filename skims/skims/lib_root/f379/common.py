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
    result: Tuple[str, ...] = tuple(
        n_id for n_id in nodes if predicate(graph.nodes[n_id])
    )
    return result


def matching_nodes_custom(graph: Graph, value: str) -> Tuple[str, ...]:
    return filter_nodes(graph, graph.nodes, pred_has_labels(value))


def is_import_used(
    graph: Graph,
    identifier: str,
) -> bool:

    vuln_nodes: List[NId] = []

    for nid_tuple in matching_nodes_custom(graph, value=identifier):
        vuln_nodes.append(nid_tuple)
    if len(vuln_nodes) > 1:
        return True
    return False


def import_is_not_used(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.matching_nodes(graph, label_type="import_specifier"):
        if alias := graph.nodes[n_id].get("label_field_alias"):
            identifier = graph.nodes[alias]["label_text"]
        else:
            name = graph.nodes[n_id]["label_field_name"]
            identifier = graph.nodes[name]["label_text"]
        if not is_import_used(graph, identifier):
            vuln_nodes.append(n_id)
    return vuln_nodes
