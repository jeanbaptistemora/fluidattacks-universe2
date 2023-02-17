from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
    get_argument,
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


def _db_no_point_in_time_recovery(graph: Graph, nid: NId) -> NId | None:
    if point := get_argument(graph, nid, "point_in_time_recovery"):
        attr, attr_val, attr_id = get_attribute(graph, point, "enabled")
        if not attr:
            return nid
        if attr_val.lower() == "false":
            return attr_id
    return None


def tfm_db_no_point_in_time_recovery(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_NO_POINT_TIME_RECOVERY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_dynamodb_table"):
                if report := _db_no_point_in_time_recovery(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f259.has_not_point_in_time_recovery",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
