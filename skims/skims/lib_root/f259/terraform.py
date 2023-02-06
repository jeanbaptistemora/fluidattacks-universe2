from lib_root.utilities.terraform import (
    get_key_value,
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


def _db_no_point_in_time_recovery(graph: Graph, nid: NId) -> Optional[NId]:
    expected_block = "point_in_time_recovery"
    expected_block_attr = "enabled"
    has_block = False
    for c_id in adj_ast(graph, nid, name=expected_block):
        for b_id in adj_ast(graph, c_id, label_type="Pair"):
            key, value = get_key_value(graph, b_id)
            if key == expected_block_attr:
                has_block = True
                if value.lower() == "false":
                    return b_id
                return None
    if not has_block:
        return nid
    return None


def tfm_db_no_point_in_time_recovery(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_NO_POINT_TIME_RECOVERY

    def n_ids() -> Iterable[GraphShardNode]:
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
