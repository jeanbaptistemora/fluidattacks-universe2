from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    FALSE_OPTIONS,
    TRUE_OPTIONS,
)
from lib_root.utilities.cloudformation import (
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


def _ec2_instance_unencrypted_ebs_block_devices(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    mappings, _, mappings_id = get_attribute(
        graph, val_id, "BlockDeviceMappings"
    )
    if mappings:
        mappings_attr = graph.nodes[mappings_id]["value_id"]
        for c_id in adj_ast(graph, mappings_attr):
            ebs, _, ebs_id = get_attribute(graph, c_id, "Ebs")
            if ebs:
                ebs_attrs = graph.nodes[ebs_id]["value_id"]
                encrypted, encrypted_val, encrypted_id = get_attribute(
                    graph, ebs_attrs, "Encrypted"
                )
                if not encrypted:
                    yield ebs_id
                elif encrypted_val not in TRUE_OPTIONS:
                    yield encrypted_id


def _ec2_has_unencrypted_volumes(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    encrypted, encrypted_val, encrypted_id = get_attribute(
        graph, val_id, "Encrypted"
    )
    if not encrypted:
        yield prop_id
    else:
        if encrypted_val in FALSE_OPTIONS:
            yield encrypted_id
        else:
            kms_key, _, _ = get_attribute(graph, val_id, "KmsKeyId")
            if not kms_key:
                yield prop_id


def cfn_ec2_has_unencrypted_volumes(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNENCRYPTED_VOLUMES

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::Volume"):
                for report in _ec2_has_unencrypted_volumes(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f250.ec2_has_unencrypted_volumes"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_instance_unencrypted_ebs_block_devices(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNENCRYPTED_BLOCK_DEVICES

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::Instance"):
                for report in _ec2_instance_unencrypted_ebs_block_devices(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "lib_path.f250.cfn_ec2_instance_unencrypted_ebs_block_devices"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
