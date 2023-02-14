from itertools import (
    chain,
)
from lib_root.utilities.terraform import (
    get_attribute,
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


def _azure_kv_only_accessible_over_https(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "https_only"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() == "false":
                return b_id
    if not has_attr:
        return nid
    return None


def _azure_sa_insecure_transfer(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "enable_https_traffic_only"
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr and value.lower() == "false":
            return b_id
    return None


def _elb2_uses_insecure_protocol(graph: Graph, nid: NId) -> Optional[NId]:
    unsafe_protos = ("HTTP",)
    pro_key, pro_val, pro_id = get_attribute(graph, nid, "protocol")
    tar_key, tar_val, _ = get_attribute(graph, nid, "target_type")
    is_proto_required = tar_val != "lambda" if tar_key else False
    if is_proto_required:
        if pro_key is None:
            return nid
        if pro_val in unsafe_protos:
            return pro_id
    return None


def tfm_elb2_uses_insecure_protocol(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_INSEC_PROTO

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lb_target_group"):
                if report := _elb2_uses_insecure_protocol(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.elb2_uses_insecure_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_only_accessible_over_https(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_ONLY_ACCESS_HTTPS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "azurerm_app_service"),
                iterate_resource(graph, "azurerm_function_app"),
            ):
                if report := _azure_kv_only_accessible_over_https(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f372.azure_only_accessible_over_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sa_insecure_transfer(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SA_INSEC_TRANSFER

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_storage_account"):
                if report := _azure_sa_insecure_transfer(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f372.tfm_azure_storage_account_insecure_transfer",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
