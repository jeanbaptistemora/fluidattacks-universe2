from collections.abc import (
    Iterator,
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


def _ebs_unencrypted_by_default(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "enabled")
    if attr and attr_val.lower() == "false":
        return attr_id
    return None


def _ebs_unencrypted_volumes(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "encrypted")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def _aux_ec2_instance_unencrypted_ebs_block_devices(
    graph: Graph, c_id: NId
) -> Iterator[NId]:
    attr, attr_val, attr_id = get_attribute(graph, c_id, "encrypted")
    if not attr:
        yield c_id
    if attr_val.lower() == "false":
        yield attr_id


def _ec2_instance_unencrypted_ebs_block_devices(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    expected_blocks = {"root_block_device", "ebs_block_device"}

    for c_id in adj_ast(graph, nid, label_type="Object"):
        if graph.nodes[c_id]["name"] in expected_blocks:
            yield from _aux_ec2_instance_unencrypted_ebs_block_devices(
                graph, c_id
            )


def tfm_ec2_instance_unencrypted_ebs_block_devices(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_UNENCRYPTED_BLOCK_DEVICES

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                for danger_id in _ec2_instance_unencrypted_ebs_block_devices(
                    graph, nid
                ):
                    yield shard, danger_id

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "lib_path.f250.tfm_ec2_instance_unencrypted_ebs_block_devices"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ebs_unencrypted_volumes(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EBS_UNENCRYPTED_VOLUMES

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_ebs_volume"):
                if report := _ebs_unencrypted_volumes(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f250.resource_not_encrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ebs_unencrypted_by_default(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EBS_UNENCRYPTED_DEFAULT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "aws_ebs_encryption_by_default"
            ):
                if report := _ebs_unencrypted_by_default(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f250.tfm_ebs_unencrypted_by_default",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
