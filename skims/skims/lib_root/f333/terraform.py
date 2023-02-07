from itertools import (
    chain,
)
from lib_root.utilities.terraform import (
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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def _ec2_has_not_an_iam_instance_profile(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "iam_instance_profile"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, _ = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
    if not has_attr:
        return nid
    return None


def _ec2_has_terminate_shutdown_behavior(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "instance_initiated_shutdown_behavior"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() != "terminate":
                return b_id
    if not has_attr:
        return nid
    return None


def _aux_ec2_associate_public_ip_address(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "associate_public_ip_address"
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr and value.lower() == "true":
            return b_id
    return None


def _ec2_associate_public_ip_address(graph: Graph, nid: NId) -> Optional[NId]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
