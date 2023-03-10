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


def iterate_resource(graph: Graph, expected_type: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        resource_type_key, resource_type_val, _ = get_attribute(
            graph, nid, "Type"
        )
        if resource_type_key and resource_type_val == expected_type:
            yield nid


def iterate_group_resources(graph: Graph, expected_type: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        resource_type_key, resource_type_val, _ = get_attribute(
            graph, nid, "Type"
        )
        if resource_type_key and expected_type in resource_type_val:
            _, _, prop_id = get_attribute(graph, nid, "Properties")
            val_id = graph.nodes[prop_id]["value_id"]
            policies, _, policies_id = get_attribute(
                graph, val_id, "ManagedPolicyArns"
            )
            if policies:
                policies_attrs = graph.nodes[policies_id]["value_id"]
                for pol in adj_ast(graph, policies_attrs):
                    yield pol


def yield_statements_from_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    statement, _, stmt_id = get_attribute(graph, nid, "Statement")
    if statement:
        stmt_attrs = graph.nodes[stmt_id]["value_id"]
        for stmt in adj_ast(graph, stmt_attrs):
            yield stmt


def _aux_iterate_iam_policy_documents(
    graph: Graph, nid: NId, resource: str
) -> Iterator[NId]:
    if resource in {
        "AWS::IAM::ManagedPolicy",
        "AWS::IAM::Policy",
        "AWS::S3::BucketPolicy",
    }:
        _, _, pd_id = get_attribute(graph, nid, "PolicyDocument")
        yield from yield_statements_from_policy(
            graph, graph.nodes[pd_id]["value_id"]
        )

    if (
        (resource in {"AWS::IAM::Role", "AWS::IAM::User"})
        and (policies := get_attribute(graph, nid, "Policies"))
        and policies[0]
    ):
        for policy in adj_ast(graph, graph.nodes[policies[2]]["value_id"]):
            _, _, pd_id = get_attribute(graph, policy, "PolicyDocument")
            yield from yield_statements_from_policy(
                graph, graph.nodes[pd_id]["value_id"]
            )

    if (
        (resource in {"AWS::IAM::Role"})
        and (document := get_attribute(graph, nid, "AssumeRolePolicyDocument"))
        and document[0]
    ):
        yield from yield_statements_from_policy(
            graph, graph.nodes[document[2]]["value_id"]
        )


def iterate_iam_policy_documents(graph: Graph) -> Iterator[NId]:
    types = ["AWS::IAM", "AWS::S3::BucketPolicy"]
    for nid in g.matching_nodes(graph, label_type="Object"):
        resource_type_key, resource_type_val, _ = get_attribute(
            graph, nid, "Type"
        )
        for res in types:
            if resource_type_key and res in resource_type_val:
                _, _, prop_id = get_attribute(graph, nid, "Properties")
                val_id = graph.nodes[prop_id]["value_id"]
                yield from _aux_iterate_iam_policy_documents(
                    graph, val_id, resource_type_val
                )


def aux_iterate_ec2_egress_ingress(
    graph: Graph, is_ingress: bool = False, is_egress: bool = False
) -> Iterator[NId]:
    if is_ingress:
        for nid in iterate_resource(graph, "AWS::EC2::SecurityGroupIngress"):
            _, _, prop_id = get_attribute(graph, nid, "Properties")
            val_id = graph.nodes[prop_id]["value_id"]
            yield val_id
    if is_egress:
        for nid in iterate_resource(graph, "AWS::EC2::SecurityGroupEgress"):
            _, _, prop_id = get_attribute(graph, nid, "Properties")
            val_id = graph.nodes[prop_id]["value_id"]
            yield val_id


def iterate_ec2_egress_ingress(
    graph: Graph, is_ingress: bool = False, is_egress: bool = False
) -> Iterator[NId]:
    for nid in iterate_resource(graph, "AWS::EC2::SecurityGroup"):
        _, _, prop_id = get_attribute(graph, nid, "Properties")
        val_id = graph.nodes[prop_id]["value_id"]
        ingress, _, ingress_id = get_attribute(
            graph, val_id, "SecurityGroupIngress"
        )
        if ingress and is_ingress:
            ingress_attrs = graph.nodes[ingress_id]["value_id"]
            for c_id in adj_ast(graph, ingress_attrs):
                yield c_id
        egress, _, egress_id = get_attribute(
            graph, val_id, "SecurityGroupEgress"
        )
        if egress and is_egress:
            ingress_attrs = graph.nodes[egress_id]["value_id"]
            for c_id in adj_ast(graph, ingress_attrs):
                yield c_id
    yield from aux_iterate_ec2_egress_ingress(graph, is_ingress, is_egress)


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False
