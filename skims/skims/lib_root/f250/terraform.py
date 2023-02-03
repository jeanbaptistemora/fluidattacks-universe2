from lib_root.utilities.json import (
    get_value,
)
from lib_root.utilities.terraform import (
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


def _ebs_unencrypted_by_default(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "enabled"
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[b_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        value_id = graph.nodes[b_id]["value_id"]
        value = get_value(graph, value_id)
        if key == expected_attr and value.lower() == "false":
            return b_id
    return None


def _ebs_unencrypted_volumes(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "encrypted"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[b_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        value_id = graph.nodes[b_id]["value_id"]
        value = get_value(graph, value_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() == "false":
                return b_id
            return None
    if not has_attr:
        return nid
    return None


def tfm_ebs_unencrypted_volumes(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EBS_UNENCRYPTED_VOLUMES

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
