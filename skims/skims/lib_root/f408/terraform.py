from collections.abc import (
    Iterator,
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
from utils.graph import (
    adj_ast,
)


def _api_gateway_access_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    expected_attr = "access_log_settings"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[b_id].get("name")
        if name == expected_attr:
            has_attr = True
    if not has_attr:
        return nid
    return None


def tfm_api_gateway_access_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_API_GATEWAY_LOGGING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_api_gateway_stage"):
                if report := _api_gateway_access_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f408.tfm_has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
