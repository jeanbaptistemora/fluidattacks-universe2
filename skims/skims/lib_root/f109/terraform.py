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


def _rds_instance_inside_subnet(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "db_subnet_group_name"
    subnet = False
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[c_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        if key == expected_attr:
            subnet = True
    if not subnet:
        return nid
    return None


def tfm_db_cluster_inside_subnet(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_INSIDE_SUBNET

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
