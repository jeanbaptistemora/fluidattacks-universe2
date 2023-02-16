from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.utilities.terraform import (
    get_argument,
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
from utils.graph import (
    adj_ast,
)


def _azure_kv_only_accessible_over_https(graph: Graph, nid: NId) -> NId | None:
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


def _azure_sa_insecure_transfer(graph: Graph, nid: NId) -> NId | None:
    expected_attr = "enable_https_traffic_only"
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr and value.lower() == "false":
            return b_id
    return None


def _elb2_uses_insecure_protocol(graph: Graph, nid: NId) -> NId | None:
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


def _aws_sec_group_using_http(graph: Graph, nid: NId) -> NId | None:
    if ingress := get_argument(graph, nid, "ingress"):
        prot_key, prot_val, prot_id = get_attribute(graph, ingress, "protocol")
        from_port_key, from_port_val, _ = get_attribute(
            graph, ingress, "from_port"
        )
        if (
            prot_key
            and prot_val in {"6", "tcp"}
            and from_port_key
            and from_port_val == "80"
        ):
            return prot_id
    return None


def aux_serves_content_over_http(
    graph: Graph, nid: NId, arg: str
) -> Iterator[NId]:
    key_cond = "viewer_protocol_policy"
    if cache := get_argument(graph, nid, arg):
        attr_key, attr_val, attr_id = get_attribute(graph, cache, key_cond)
        if attr_key and attr_val == "allow-all":
            yield attr_id


def _serves_content_over_http(graph: Graph, nid: NId) -> Iterator[NId]:
    yield from aux_serves_content_over_http(
        graph, nid, "default_cache_behavior"
    )
    yield from aux_serves_content_over_http(
        graph, nid, "ordered_cache_behavior"
    )


def tfm_serves_content_over_http(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CONTENT_HTTP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_cloudfront_distribution"):
                for report in _serves_content_over_http(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.serves_content_over_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_sec_group_using_http(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_SEC_GROUP_USING_HTTP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_security_group"):
                if report := _aws_sec_group_using_http(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f372.tfm_aws_sec_group_using_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_elb2_uses_insecure_protocol(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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
