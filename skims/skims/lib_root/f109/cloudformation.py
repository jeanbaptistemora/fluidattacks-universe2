from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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


def _rds_is_not_inside_a_db_subnet_group(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    group_name, _, _ = get_attribute(graph, val_id, "DBSubnetGroupName")
    if not group_name:
        yield prop_id


def cfn_rds_is_not_inside_a_db_subnet_group(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_INSIDE_DB_SUBNET

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "AWS::RDS::DBCluster"),
                iterate_resource(graph, "AWS::RDS::DBInstance"),
            ):
                for report in _rds_is_not_inside_a_db_subnet_group(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f109.rds_is_not_inside_a_db_subnet_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
