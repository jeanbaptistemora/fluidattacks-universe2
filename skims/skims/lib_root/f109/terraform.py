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


def _rds_instance_inside_subnet(graph: Graph, nid: NId) -> NId | None:
    attr = get_attribute(graph, nid, "db_subnet_group_name")
    if not attr[0]:
        return nid
    return None


def tfm_db_cluster_inside_subnet(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_INSIDE_SUBNET

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_db_instance"):
                if report := _rds_instance_inside_subnet(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f109.rds_is_not_inside_a_db_subnet_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_rds_instance_inside_subnet(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_INSIDE_SUBNET

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_rds_cluster"):
                if report := _rds_instance_inside_subnet(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f109.rds_is_not_inside_a_db_subnet_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
