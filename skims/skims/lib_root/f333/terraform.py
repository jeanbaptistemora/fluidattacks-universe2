from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.utilities.terraform import (
    get_attribute,
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


def _ec2_has_not_an_iam_instance_profile(graph: Graph, nid: NId) -> NId | None:
    attr, _, _ = get_attribute(graph, nid, "iam_instance_profile")
    if not attr:
        return nid
    return None


def _ec2_has_terminate_shutdown_behavior(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "instance_initiated_shutdown_behavior"
    )
    if not attr:
        return nid
    if attr_val.lower() != "terminate":
        return attr_id
    return None


def _aux_ec2_associate_public_ip_address(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "associate_public_ip_address"
    )
    if attr and attr_val.lower() == "true":
        return attr_id
    return None


def _ec2_associate_public_ip_address(graph: Graph, nid: NId) -> NId | None:
    obj_type = graph.nodes[nid].get("name")
    if obj_type and obj_type == "aws_instance":
        return _aux_ec2_associate_public_ip_address(graph, nid)
    expected_block = "network_interfaces"
    for c_id in adj_ast(graph, nid, name=expected_block):
        return _aux_ec2_associate_public_ip_address(graph, c_id)
    return None


def tfm_ec2_associate_public_ip_address(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_ASSOC_PUB_IP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_instance"),
                iterate_resource(graph, "aws_launch_template"),
            ):
                if report := _ec2_associate_public_ip_address(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.ec2_public_ip_addresses",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_terminate_shutdown_behavior(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.EC2_TERMINATE_SHUTDOWN_BEHAVIOR

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_launch_template"):
                if report := _ec2_has_terminate_shutdown_behavior(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.tfm_ec2_allows_shutdown_command",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_not_an_iam_instance_profile(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_NO_IAM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                if report := _ec2_has_not_an_iam_instance_profile(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f333.ec2_has_not_an_iam_instance_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
