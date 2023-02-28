from collections.abc import (
    Iterator,
)
from lib_root.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
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


def _elb2_uses_insecure_security_policy(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    ssl_policy, ssl_val, ssl_id = get_attribute(graph, val_id, "SslPolicy")

    if (
        ssl_policy
        and ssl_val in PREDEFINED_SSL_POLICY_VALUES
        and ssl_val not in SAFE_SSL_POLICY_VALUES
    ):
        yield ssl_id


def _elb2_target_group_insecure_port(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    properties_id = graph.nodes[prop_id]["value_id"]
    port, port_val, port_id = get_attribute(graph, properties_id, "Port")
    _, target_type, _ = get_attribute(graph, properties_id, "TargetType")
    if target_type != "lambda":
        if not port:
            yield prop_id
        elif int(port_val) != 443:
            yield port_id


def cfn_elb2_target_group_insecure_port(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_LB_TARGET_INSECURE_PORT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::TargetGroup"
            ):
                for report in _elb2_target_group_insecure_port(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f070.elb2_target_group_insecure_port",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_elb2_uses_insecure_security_policy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_INSECURE_SEC_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::Listener"
            ):
                for report in _elb2_uses_insecure_security_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
