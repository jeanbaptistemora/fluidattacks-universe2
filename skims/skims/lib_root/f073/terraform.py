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


def _db_instance_publicly_accessible(graph: Graph, nid: NId) -> NId | None:
    if attr := get_attribute(graph, nid, "publicly_accessible"):
        if attr[0] and attr[1] == "true":
            return attr[2]
    return None


def tfm_db_instance_publicly_accessible(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_PUB_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_db_instance"):
                if report := _db_instance_publicly_accessible(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f073.cfn_rds_is_publicly_accessible",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_db_cluster_publicly_accessible(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_CLUSTER_PUB_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_rds_cluster_instance"):
                if report := _db_instance_publicly_accessible(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f073.cfn_rds_is_publicly_accessible",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
