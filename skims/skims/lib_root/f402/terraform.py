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


def _azure_app_service_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    if logs := get_argument(graph, nid, "logs"):
        fail_key, fail_val, _ = get_attribute(
            graph, logs, "failed_request_tracing_enabled"
        )
        det_key, det_val, _ = get_attribute(
            graph, logs, "detailed_error_messages_enabled"
        )
        if (not fail_key or fail_val.lower() == "false") or (
            not det_key or det_val.lower() == "false"
        ):
            return logs
    else:
        return nid
    return None


def _azure_sql_server_audit_log_retention(
    graph: Graph, nid: NId
) -> NId | None:
    if logs := get_argument(graph, nid, "extended_auditing_policy"):
        ret_key, ret_val, attr_id = get_attribute(
            graph, logs, "retention_in_days"
        )
        if not ret_key:
            return logs
        if ret_val.isdigit() and int(ret_val) <= 90:
            return attr_id
    else:
        return nid
    return None


def _azure_storage_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    if queue := get_argument(graph, nid, "queue_properties"):
        if logging := get_argument(graph, queue, "logging"):
            attrs = [
                get_attribute(graph, logging, req)
                for req in ["delete", "read", "write"]
            ]
            if not all(
                (
                    val.lower() == "true" if req else False
                    for req, val, _ in attrs
                )
            ):
                return logging
        else:
            return queue
    else:
        return nid
    return None


def tfm_azure_storage_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_STORAGE_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_storage_account"):
                if report := _azure_storage_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f402.tfm_azure_storage_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sql_server_audit_log_retention(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SQL_LOG_RETENT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_sql_server"):
                if report := _azure_sql_server_audit_log_retention(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f402.tfm_azure_sql_server_audit_log_retention",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_app_service_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_APP_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
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
