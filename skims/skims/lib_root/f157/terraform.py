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
from utils.graph import (
    adj_ast,
)


def _aux_azure_sa_default_network_access(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "default_action")
    if not attr:
        return nid
    if attr_val.lower() != "deny":
        return attr_id
    return None


def _azure_sa_default_network_access(graph: Graph, nid: NId) -> NId | None:
    obj_type = graph.nodes[nid].get("name")
    if obj_type:
        if obj_type == "azurerm_storage_account_network_rules":
            return _aux_azure_sa_default_network_access(graph, nid)
        expected_block = "network_rules"
        for c_id in adj_ast(graph, nid, name=expected_block):
            return _aux_azure_sa_default_network_access(graph, c_id)
    return None


def _aws_acl_broad_network_access(graph: Graph, nid: NId) -> NId | None:
    danger_values = {
        "::/0",
        "0.0.0.0/0",
    }
    if ingress := get_argument(graph, nid, "ingress"):
        attr, attr_val, attr_id = get_attribute(graph, ingress, "cidr_block")
        if attr and attr_val in danger_values:
            return attr_id
    return None


def _azure_kv_danger_bypass(graph: Graph, nid: NId) -> NId | None:
    if network := get_argument(graph, nid, "network_acls"):
        attr, attr_val, attr_id = get_attribute(graph, network, "bypass")
        if not attr:
            return nid
        if attr_val.lower() != "azureservices":
            return attr_id
    return None


def _azure_kv_default_network_access(graph: Graph, nid: NId) -> NId | None:
    if network := get_argument(graph, nid, "network_acls"):
        attr, attr_val, attr_id = get_attribute(
            graph, network, "default_action"
        )
        if not attr:
            return nid
        if attr_val.lower() != "deny":
            return attr_id
    return None


def _azure_unrestricted_access_network_segments(
    graph: Graph, nid: NId
) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "public_network_enabled"
    )
    if not attr:
        return nid
    if attr_val.lower() == "true":
        return attr_id
    return None


def tfm_aws_acl_broad_network_access(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_ACL_BROAD_NETWORK_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_default_network_acl"):
                if report := _aws_acl_broad_network_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f157.tfm_aws_acl_broad_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_danger_bypass(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_DANGER_BYPASS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_key_vault"):
                if report := _azure_kv_danger_bypass(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f157.tfm_azure_kv_danger_bypass",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_default_network_access(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_DEFAULT_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_key_vault"):
                if report := _azure_kv_default_network_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f157.tfm_azure_kv_default_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_unrestricted_access_network_segments(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_UNRESTRICTED_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_data_factory"):
                if report := _azure_unrestricted_access_network_segments(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f157.etl_visible_to_the_public_network",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sa_default_network_access(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SA_DEFAULT_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(
                    graph, "azurerm_storage_account_network_rules"
                ),
                iterate_resource(graph, "azurerm_storage_account"),
            ):
                if report := _azure_sa_default_network_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f157.tfm_azure_sa_default_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
