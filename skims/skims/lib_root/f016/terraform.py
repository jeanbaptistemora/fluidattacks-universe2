from lib_root.utilities.terraform import (
    get_argument,
    get_attr_from_block,
    get_attribute,
    get_key_value,
    iterate_resource,
    list_has_string,
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
    Iterator,
    Optional,
)
from utils.graph import (
    adj_ast,
)

VULNERABLE_ORIGIN_SSL_PROTOCOLS = ["SSLv3", "TLSv1", "TLSv1.1"]


VULNERABLE_MIN_PROT_VERSIONS = [
    "SSLv3",
    "TLSv1",
    "TLSv1_2016",
    "TLSv1.1_2016",
]


def _azure_serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "min_tls_version"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, c_id)
        if key == expected_attr:
            if value in ("TLS1_0", "TLS1_1"):
                return c_id
            return None
    return nid


def _aws_elb_without_sslpolicy(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "ssl_policy"
    is_vuln = True
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, _ = get_key_value(graph, c_id)
        if key == expected_attr:
            is_vuln = False
    if is_vuln:
        return nid
    return None


def has_vuln_ssl(graph: Graph, nid: NId) -> bool:
    array_id = graph.nodes[nid]["value_id"]
    for prot in VULNERABLE_ORIGIN_SSL_PROTOCOLS:
        if list_has_string(graph, array_id, prot):
            return True
    return False


def _aws_serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if (v_cert := get_argument(graph, nid, "viewer_certificate")) and (
        (min_prot := get_attribute(graph, v_cert, "minimum_protocol_version"))
        and any(
            True
            for protocol in VULNERABLE_MIN_PROT_VERSIONS
            if protocol == min_prot[1]
        )
    ):
        yield min_prot[2]
    if (origin := get_argument(graph, nid, "origin")) and (
        (
            ssl_prot := get_attr_from_block(
                graph, origin, "custom_origin_config", "origin_ssl_protocols"
            )
        )
        and has_vuln_ssl(graph, ssl_prot[2])
    ):
        yield ssl_prot[2]


def tfm_aws_serves_content_over_insecure_protocols(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_INSEC_PROTO

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_cloudfront_distribution"):
                for report in _aws_serves_content_over_insecure_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_serves_content_over_insecure_protocols(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_INSEC_PROTO

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_storage_account"):
                if report := _azure_serves_content_over_insecure_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_elb_without_sslpolicy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_ELB_WITHOUT_SSLPOLICY

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lb_listener"):
                if report := _aws_elb_without_sslpolicy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f016.aws_elb_without_sslpolicy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
