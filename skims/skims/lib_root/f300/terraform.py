from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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


def _azure_app_authentication_off(graph: Graph, nid: NId) -> NId | None:
    if auth := get_argument(graph, nid, "auth_settings"):
        attr, attr_val, attr_id = get_attribute(graph, auth, "enabled")
        if not attr:
            return auth
        if attr_val.lower() == "false":
            return attr_id
    else:
        return nid
    return None


def _azure_as_client_certificates_enabled(
    graph: Graph, nid: NId
) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "client_cert_enabled")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def tfm_azure_as_client_certificates_enabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_CLIENT_CERT_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_app_service"):
                if report := _azure_as_client_certificates_enabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f300.tfm_azure_as_client_certificates_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_app_authentication_off(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_APP_AUTH_OFF

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "azurerm_app_service"),
                iterate_resource(graph, "azurerm_function_app"),
            ):
                if report := _azure_app_authentication_off(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f300.tfm_azure_app_authentication_off",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
