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


def _trail_log_files_not_validated(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "enable_log_file_validation"
    )
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
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
