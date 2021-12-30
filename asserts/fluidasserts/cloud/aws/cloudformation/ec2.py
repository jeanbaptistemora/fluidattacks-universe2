# pylint: disable=too-many-lines
"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


import contextlib
from fluidasserts import (
    HIGH,
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_predecessor,
    get_ref_nodes,
    get_templates,
    get_type,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.helper.aws import (
    CloudFormationInvalidTypeError,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from ipaddress import (
    IPv4Network,
    IPv6Network,
)
import networkx as nx
from networkx import (
    DiGraph,
)
from networkx.algorithms import (
    dfs_preorder_nodes,
)
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


def _iterate_security_group_rules(graph: DiGraph, group: int):
    """Iterate over the different security groups entities in the template."""
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    cidrs: List[int] = [
        node
        for node in dfs_preorder_nodes(graph, group, 10)
        if graph.nodes[node]["labels"].intersection({"CidrIp", "CidrIpv6"})
    ]

    rules = []
    for cidr in cidrs:
        cidr_node = get_ref_nodes(graph, cidr, helper.is_cidr)
        if not cidr_node:
            continue
        cidr_node = cidr_node[0]

        father = list(graph.predecessors(cidr))[0]
        from_port_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(
                    graph, node, lambda y: isinstance(y, (int, float))
                )
                for node in dfs_preorder_nodes(graph, father, 1)
                if "FromPort" in graph.nodes[node]["labels"]
            ]
        )

        to_port_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(
                    graph, node, lambda y: isinstance(y, (int, float))
                )
                for node in dfs_preorder_nodes(graph, father, 1)
                if "ToPort" in graph.nodes[node]["labels"]
            ]
        )

        ip_protocol_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(graph, node, helper.is_ip_protocol)
                for node in dfs_preorder_nodes(graph, father, 1)
                if "IpProtocol" in graph.nodes[node]["labels"]
            ]
        )

        if not from_port_node or not to_port_node or not ip_protocol_node:
            continue

        from_port_node = from_port_node[0]
        to_port_node = to_port_node[0]
        ip_protocol_node = ip_protocol_node[0]
        _type: str = get_type(
            graph, get_predecessor(graph, cidr, allow_groups), allow_groups
        )
        rule = {
            "FromPort": from_port_node,
            "ToPort": to_port_node,
            get_type(graph, cidr, {"CidrIp", "CidrIpv6"}): cidr_node,
            "IpProtocol": ip_protocol_node,
            "type": _type,
        }
        rules.append(rule)

    return rules


def _get_securitygroups(
    graph: DiGraph, path: str, exclude: Optional[List[str]] = None
) -> List[int]:
    templates: List[int] = get_templates(graph, path, exclude)
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    return [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if graph.nodes[node]["labels"].intersection(
            {"SecurityGroup", *allow_groups}
        )
    ]


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_cidrs(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if any ``EC2::SecurityGroup`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param graph: Templates converted into a DiGraph.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    allow_groups = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[Dict] = _get_securitygroups(graph, path, exclude)
    for group in security_groups:
        template: Dict = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        resource: Dict = graph.nodes[group]
        rules: List[Dict] = _iterate_security_group_rules(graph, group)

        for rule in rules:
            cidr_ip = None
            ip_object: [Union[IPv4Network, IPv6Network]] = None
            _type: str = rule["type"]
            entities: List[Tuple] = []
            if rule.get("CidrIp", None):
                cidr_ip = rule["CidrIp"]
                ip_value = graph.nodes[rule["CidrIp"]]["value"]
                ip_object: IPv4Network = IPv4Network(ip_value, strict=False)
                if ip_object == unrestricted_ipv4:
                    entities.append(
                        (f"CidrIp/{ip_value}", "must not be 0.0.0.0/0")
                    )
                if (
                    _type == "SecurityGroupIngress"
                    and ip_object.num_addresses > 1
                ):
                    entities.append(
                        (f"CidrIp/{ip_value}", "must use /32 subnet mask")
                    )
            elif rule.get("CidrIpv6", None):
                cidr_ip = rule["CidrIpv6"]
                ip_value = graph.nodes[rule["CidrIpv6"]]["value"]
                ip_object: IPv4Network = IPv6Network(ip_value, strict=False)
                if ip_object == unrestricted_ipv6:
                    entities.append(
                        (f"CidrIpv6/{ip_value}", "must not be ::/0")
                    )
                if (
                    _type == "SecurityGroupIngress"
                    and ip_object.num_addresses > 1
                ):
                    entities.append(
                        (f"CidrIpv6/{ip_value}", "must use /128 subnet mask")
                    )

            ip_node: int = graph.nodes[cidr_ip]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )

            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"AWS::EC2::{resource_type}/{entity}'",
                    identifier=resource["name"],
                    line=ip_node["line"],
                    reason=reason,
                )
                for entity, reason in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 security groups have unrestricted CIDRs",
        msg_closed="EC2 security groups do not have unrestricted CIDRs",
    )
