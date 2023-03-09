from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.utilities.cloudformation import (
    get_attribute,
    iterate_ec2_egress_ingress,
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


def _instances_without_profile(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    instance_profile, _, _ = get_attribute(graph, val_id, "IamInstanceProfile")
    if not instance_profile:
        yield prop_id


def _groups_without_egress(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    egress, _, _ = get_attribute(graph, val_id, "SecurityGroupEgress")
    if not egress:
        yield prop_id


def _unrestricted_ip_protocols(graph: Graph, nid: NId) -> Iterator[NId]:
    ip_protocol, ip_protocol_val, ip_protocol_id = get_attribute(
        graph, nid, "IpProtocol"
    )
    if ip_protocol and ip_protocol_val in (-1, "-1"):
        yield ip_protocol_id


def _ec2_has_unrestricted_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    from_port, from_port_val, from_port_id = get_attribute(
        graph, nid, "FromPort"
    )
    to_port, to_port_val, _ = get_attribute(graph, nid, "ToPort")
    if (
        from_port
        and to_port
        and int(from_port_val) != int(to_port_val)
        and abs(int(to_port_val) - int(from_port_val)) > 25
    ):
        yield from_port_id


def _ec2_has_unrestricted_ftp_access(graph: Graph, nid: NId) -> Iterator[NId]:
    public_cidrs = {
        "::/0",
        "0.0.0.0/0",
    }
    cidr, cidr_val, _ = get_attribute(graph, nid, "CidrIp")
    if not cidr:
        cidr, cidr_val, _ = get_attribute(graph, nid, "CidrIpv6")
    is_public_cidr = cidr_val in public_cidrs
    from_port, from_port_val, from_port_id = get_attribute(
        graph, nid, "FromPort"
    )
    to_port, to_port_val, _ = get_attribute(graph, nid, "ToPort")
    if is_public_cidr and to_port and from_port:
        for port in range(20, 22):
            _, ip_protocol_val, _ = get_attribute(graph, nid, "IpProtocol")
            if float(from_port_val) <= port <= float(
                to_port_val
            ) and ip_protocol_val in ("tcp", "-1"):
                yield from_port_id


def cfn_ec2_has_unrestricted_ftp_access(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNRESTRICTED_FTP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_ec2_egress_ingress(
                graph, is_ingress=True, is_egress=True
            ):
                for report in _ec2_has_unrestricted_ftp_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024.ec2_has_unrestricted_ftp_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_unrestricted_ports(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNRESTRICTED_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_ec2_egress_ingress(
                graph, is_ingress=True, is_egress=True
            ):
                for report in _ec2_has_unrestricted_ports(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024.ec2_has_unrestricted_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_unrestricted_ip_protocols(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_UNRESTRICTED_IP_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_ec2_egress_ingress(
                graph, is_ingress=True, is_egress=True
            ):
                for report in _unrestricted_ip_protocols(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.unrestricted_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_groups_without_egress(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_GROUPS_WITHOUT_EGRESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::SecurityGroup"):
                for report in _groups_without_egress(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.security_group_without_egress",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_instances_without_profile(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INST_WITHOUT_PROFILE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::Instance"):
                for report in _instances_without_profile(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
