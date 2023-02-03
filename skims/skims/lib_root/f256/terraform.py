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


def _has_not_automated_backups(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "backup_retention_period"
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[b_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        value_id = graph.nodes[b_id]["value_id"]
        value = get_value(graph, value_id)
        if key == expected_attr and value == "0":
            return b_id
    return None


def _no_deletion_protection(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "deletion_protection"
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


def tfm_rds_no_deletion_protection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_NO_DELETION_PROTEC

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_rds_cluster"):
                if report := _no_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f256.rds_has_not_termination_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_rds_has_not_automated_backups(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_NOT_AUTO_BACKUPS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_rds_cluster"):
                if report := _has_not_automated_backups(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f256.rds_has_not_automated_backups",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_db_has_not_automated_backups(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_NOT_AUTO_BACKUPS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_db_instance"):
                if report := _has_not_automated_backups(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f256.rds_has_not_automated_backups",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
