from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
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


def _rds_is_publicly_accessible(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    public_acces, public_val, public_id = get_attribute(
        graph, val_id, "PubliclyAccessible"
    )
    if public_acces and public_val in TRUE_OPTIONS:
        yield public_id


def cfn_rds_is_publicly_accessible(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_PUB_ACCESSIBLE

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
                for report in _rds_is_publicly_accessible(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f073.cfn_rds_is_publicly_accessible",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
