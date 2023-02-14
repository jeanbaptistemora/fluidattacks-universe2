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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def get_argument(graph: Graph, nid: NId, expected_block: str) -> Optional[str]:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[block_id].get("name")
        if name == expected_block:
            return block_id
    return None


def _azure_app_service_logging_disabled(
    graph: Graph, nid: NId
) -> Optional[NId]:
    if logs := get_argument(graph, nid, "logs"):
        fail_key, fail_val = get_attribute(
            graph, logs, "failed_request_tracing_enabled"
        )
        det_key, det_val = get_attribute(
            graph, logs, "detailed_error_messages_enabled"
        )
        if (not fail_key or fail_val.lower() == "false") or (
            not det_key or det_val.lower() == "false"
        ):
            return logs
    return None


def tfm_azure_app_service_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_APP_LOG_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_app_service"):
                if report := _azure_app_service_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f402.tfm_azure_failed_request_tracing_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
