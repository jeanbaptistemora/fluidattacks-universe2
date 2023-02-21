from collections.abc import (
    Iterator,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from model.graph_model import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def get_list_from_node(graph: Graph, nid: NId) -> list:
    if graph.nodes[nid]["label_type"] == "ArrayInitializer":
        child_ids = adj_ast(graph, nid)
        result: list = []
        for c_id in child_ids:
            result.append(graph.nodes[c_id].get("value"))
        return result
    return [graph.nodes[nid].get("value")]


def get_principals(graph: Graph, stmt: NId) -> str:
    principal = get_argument(graph, stmt, "principals")
    if principal:
        types, type_val, _ = get_attribute(graph, principal, "type")
        identifier, _, identifier_id = get_attribute(
            graph, principal, "identifiers"
        )
        identifier_list = get_list_from_node(
            graph, graph.nodes[identifier_id]["value_id"]
        )
        if not identifier or not types:
            return ""
        if type_val == "*" and "*" in identifier_list:
            return "*"
    return ""


def iter_statements_from_policy_document(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[block_id].get("name")
        if name == "statement":
            yield block_id


def get_attr_inside_attrs(
    graph: Graph, nid: NId, attrs: list
) -> tuple[str | None, str, NId]:
    curr_nid = nid
    final_key, final_val, final_id = None, "", ""
    attr, attr_val, attr_id = None, "", ""
    for key in attrs:
        if not curr_nid:
            break
        attr, attr_val, attr_id = get_attribute(graph, curr_nid, key)
        if not attr:
            break
        curr_nid = graph.nodes[attr_id].get("value_id")
    else:
        final_key, final_val, final_id = attr, attr_val, attr_id

    return final_key, final_val, final_id


def is_cidr(cidr: str) -> bool:
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def get_attr_from_block(
    graph: Graph, nid: NId, expected_block: str, expected_attr: str
) -> tuple[str | None, str, NId] | None:
    if argument := get_argument(graph, nid, expected_block):
        attr_key, _, attr_id = get_attribute(graph, argument, expected_attr)
        if attr_key:
            return attr_key, "", attr_id
    return None


def get_argument(graph: Graph, nid: NId, expected_block: str) -> str | None:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[block_id].get("name")
        if name == expected_block:
            return block_id
    return None


def get_key_value(graph: Graph, nid: NId) -> tuple[str, str]:
    key_id = graph.nodes[nid]["key_id"]
    key = graph.nodes[key_id]["value"]
    value_id = graph.nodes[nid]["value_id"]
    value = ""
    if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
        child_id = adj_ast(graph, value_id, label_type="Literal")
        if len(child_id) > 0:
            value = graph.nodes[child_id[0]].get("value", "")
    else:
        value = graph.nodes[value_id].get("value", "")
    return key, value


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str | None, str, NId]:
    if object_id != "":
        for attr_id in adj_ast(graph, object_id, label_type="Pair"):
            key, value = get_key_value(graph, attr_id)
            if key == expected_attr:
                return key, value, attr_id
    return None, "", ""


def iterate_resource(graph: Graph, expected_resource: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        name = graph.nodes[nid].get("name")
        if name and name == expected_resource:
            yield nid


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False
