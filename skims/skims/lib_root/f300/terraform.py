from itertools import (
    chain,
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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def _azure_app_authentication_off(graph: Graph, nid: NId) -> Optional[NId]:
    expected_block = "auth_settings"
    expected_block_attr = "enabled"
    has_attr = False
    has_block = False
    for c_id in adj_ast(graph, nid, name=expected_block):
        has_block = True
        for b_id in adj_ast(graph, c_id, label_type="Pair"):
            key, value = get_key_value(graph, b_id)
            if key == expected_block_attr:
                has_attr = True
                if value.lower() == "false":
                    return b_id
                return None
        if not has_attr:
            return c_id
    if not has_block:
        return nid
    return None


def _azure_as_client_certificates_enabled(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "client_cert_enabled"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() == "false":
                return b_id
            return None
    if not has_attr:
        return nid
    return None


def tfm_azure_as_client_certificates_enabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_CLIENT_CERT_ENABLED

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
