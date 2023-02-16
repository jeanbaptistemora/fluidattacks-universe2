from collections.abc import (
    Iterator,
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
from utils.graph import (
    adj_ast,
)


def _aws_ebs_volumes_unencrypted(graph: Graph, nid: NId) -> NId | None:
    expected_block = "root_block_device"
    expected_block_attr = "encrypted"
    has_block = False
    has_attr = False
    for c_id in adj_ast(graph, nid, name=expected_block):
        has_block = True
        for b_id in adj_ast(graph, c_id, label_type="Pair"):
            key, value = get_key_value(graph, b_id)
            if key == expected_block_attr:
                has_attr = True
                if value.lower() == "false":
                    return b_id
                return None
        if not has_attr:
            return c_id
    if not has_block:
        return nid
    return None


def tfm_aws_ebs_volumes_unencrypted(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EBS_VOLUMES_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_launch_configuration"):
                if report := _aws_ebs_volumes_unencrypted(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f407.tfm_aws_ebs_volumes_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
