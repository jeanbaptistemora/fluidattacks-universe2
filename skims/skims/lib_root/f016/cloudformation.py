from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.f016.terraform import (
    VULNERABLE_MIN_PROT_VERSIONS,
    VULNERABLE_ORIGIN_SSL_PROTOCOLS,
)
from lib_root.utilities.cloudformation import (
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
    match_ast_d,
)


def _elb_without_sslpolicy(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if not get_attribute(graph, val_id, "SslPolicy")[0]:
        yield nid


def _helper_insecure_protocols(graph: Graph, nid: NId) -> Iterator[NId]:
    object_id = match_ast_d(graph, nid, "Object")
    if object_id:
        custom_origin, _, co_id = get_attribute(
            graph, object_id, "CustomOriginConfig"
        )
        if custom_origin:
            custom_attrs = graph.nodes[co_id]["value_id"]
            ssl_prot, _, ssl_prot_id = get_attribute(
                graph, custom_attrs, "OriginSSLProtocols"
            )
            if ssl_prot:
                ssl_list_id = graph.nodes[ssl_prot_id]["value_id"]
                for c_id in adj_ast(graph, ssl_list_id):
                    if (
                        graph.nodes[c_id].get("value")
                        in VULNERABLE_ORIGIN_SSL_PROTOCOLS
                    ):
                        yield c_id


def _serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    dist_config, _, dist_id = get_attribute(
        graph, val_id, "DistributionConfig"
    )
    if dist_config:
        dist_attrs = graph.nodes[dist_id]["value_id"]
        v_cert, _, v_id = get_attribute(graph, dist_attrs, "ViewerCertificate")
        if v_cert:
            v_attrs = graph.nodes[v_id]["value_id"]
            _, min_proto, min_proto_id = get_attribute(
                graph, v_attrs, "MinimumProtocolVersion"
            )
            if min_proto in VULNERABLE_MIN_PROT_VERSIONS:
                yield min_proto_id
        origins, _, origins_id = get_attribute(graph, dist_attrs, "Origins")
        if origins:
            origin_attr = graph.nodes[origins_id]["value_id"]
            yield from _helper_insecure_protocols(graph, origin_attr)


def cfn_serves_content_over_insecure_protocols(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::CloudFront::Distribution"
            ):
                for report in _serves_content_over_insecure_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_elb_without_sslpolicy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB_WITHOUT_SSLPOLICY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::Listener"
            ):
                for report in _elb_without_sslpolicy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f016.aws_elb_without_sslpolicy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
