from collections.abc import (
    Iterator,
)
from lib_root.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
)
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


def _lb_target_group_insecure_port(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "port")
    if not attr:
        return nid
    if attr_val != "443":
        return attr_id
    return None


def _elb2_uses_insecure_security_policy(graph: Graph, nid: NId) -> NId | None:
    if attr := get_attribute(graph, nid, "ssl_policy"):
        if (
            attr[0]
            and attr[1] in PREDEFINED_SSL_POLICY_VALUES
            and attr[1] not in SAFE_SSL_POLICY_VALUES
        ):
            return attr[2]
    return None


def tfm_lb_target_group_insecure_port(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_LB_TARGET_INSECURE_PORT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lb_target_group"):
                if report := _lb_target_group_insecure_port(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f070.elb2_target_group_insecure_port",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_elb2_uses_insecure_security_policy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_INSECURE_SEC_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lb_listener"):
                if report := _elb2_uses_insecure_security_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
