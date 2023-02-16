from collections.abc import (
    Iterator,
)
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
from utils.graph import (
    adj_ast,
)


def _trail_log_files_not_validated(graph: Graph, nid: NId) -> NId | None:
    expected_attr = "enable_log_file_validation"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() in {"false", "0"}:
                return b_id
    if not has_attr:
        return nid
    return None


def tfm_trail_log_files_not_validated(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CTRAIL_LOG_NOT_VALIDATED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_cloudtrail"):
                if report := _trail_log_files_not_validated(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f394.tfm_log_files_not_validated",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
