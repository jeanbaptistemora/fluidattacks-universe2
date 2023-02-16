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


def _has_unencrypted_storage(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "storage_encrypted")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def tfm_rds_has_unencrypted_storage(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_UNENCRYPTED_STORAGE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_rds_cluster"):
                if report := _has_unencrypted_storage(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f246.rds_has_unencrypted_storage",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_db_has_unencrypted_storage(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_UNENCRYPTED_STORAGE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_db_instance"):
                if report := _has_unencrypted_storage(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f246.rds_has_unencrypted_storage",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
