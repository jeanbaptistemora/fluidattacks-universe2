from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    FALSE_OPTIONS,
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


def _rds_has_not_termination_protection(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    deletion_prot, del_val, del_id = get_attribute(
        graph, val_id, "DeletionProtection"
    )
    if not deletion_prot:
        yield prop_id
    elif del_val in FALSE_OPTIONS:
        yield del_id


def _rds_has_not_automated_backups(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    backup, backup_val, backup_id = get_attribute(
        graph, val_id, "BackupRetentionPeriod"
    )
    if backup and backup_val in (0, "0"):
        yield backup_id


def cfn_rds_has_not_automated_backups(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_AUTO_BACKUPS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "AWS::RDS::DBCluster"),
                iterate_resource(graph, "AWS::RDS::DBInstance"),
            ):
                for report in _rds_has_not_automated_backups(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f256.rds_has_not_automated_backups",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_rds_has_not_termination_protection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_TERMINATION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "AWS::RDS::DBCluster"),
                iterate_resource(graph, "AWS::RDS::DBInstance"),
            ):
                for report in _rds_has_not_termination_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f256.rds_has_not_termination_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
