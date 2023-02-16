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
from itertools import (
    chain,
)
from lib_root.f024.constants import (
    ADMIN_PORTS,
    UNRESTRICTED_IPV4,
    UNRESTRICTED_IPV6,
)
from lib_root.utilities.terraform import (
    get_attribute,
    get_key_value,
    iterate_resource,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.graph import (
    adj_ast,
)


def _ec2_instances_without_profile(graph: Graph, nid: NId) -> NId | None:
    expected_attr = "iam_instance_profile"
    is_vuln = True
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, _ = get_key_value(graph, c_id)
        if key == expected_attr:
            is_vuln = False
    if is_vuln:
        return nid
    return None


def _aws_ec2_allows_all_outbound_traffic(graph: Graph, nid: NId) -> NId | None:
    expected_block = "egress"
    if len(adj_ast(graph, nid, name=expected_block)) == 0:
        return nid
    return None


def _aws_allows_anyone_to_admin_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    unrestricted_ip = False
    cidr_ip, cidr_ip_val, _ = get_attribute(graph, nid, "cidr_blocks")
    cidr_ipv6, cidr_ipv6_val, _ = get_attribute(graph, nid, "ipv6_cidr_blocks")
    with suppress(AddressValueError, KeyError):
        unrestricted_ip = (
            cidr_ipv6 is not None
            and IPv6Network(
                cidr_ipv6_val,
                strict=False,
            )
            == UNRESTRICTED_IPV6
        )
    with suppress(AddressValueError, KeyError):
        unrestricted_ip = (
            IPv4Network(
                cidr_ip_val,
                strict=False,
            )
            == UNRESTRICTED_IPV4
            if cidr_ip
            else unrestricted_ip
        ) or unrestricted_ip
    from_port, from_port_val, from_port_id = get_attribute(
        graph, nid, "from_port"
    )
    to_port, to_port_val, to_port_id = get_attribute(graph, nid, "to_port")
    port_range = (
        set(
            range(
                int(from_port_val),
                int(to_port_val) + 1,
            )
        )
        if from_port and to_port
        else set()
    )
    if unrestricted_ip and ADMIN_PORTS.intersection(port_range):
        yield from_port_id
        yield to_port_id


def tfm_aws_allows_anyone_to_admin_ports(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ANYONE_ADMIN_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_security_group"),
                iterate_resource(graph, "aws_security_group_rule"),
                iterate_resource(graph, "ingress"),
            ):
                for report in _aws_allows_anyone_to_admin_ports(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.allows_anyone_to_admin_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_instances_without_profile(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_INST_WITHOUT_PROFILE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                if report := _ec2_instances_without_profile(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_ec2_allows_all_outbound_traffic(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EC2_ALL_TRAFFIC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_security_group"):
                if report := _aws_ec2_allows_all_outbound_traffic(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.security_group_without_egress",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
