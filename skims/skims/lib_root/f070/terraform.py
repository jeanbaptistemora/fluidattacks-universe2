from lib_path.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
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


def _lb_target_group_insecure_port(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "port"
    is_vuln = True
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, c_id)
        if key == expected_attr:
            if value == "443":
                is_vuln = False
            else:
                return c_id
    if is_vuln:
        return nid
    return None


def _elb2_uses_insecure_security_policy(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "ssl_policy"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, c_id)
        if key == expected_attr and (
            value in PREDEFINED_SSL_POLICY_VALUES
            and value not in SAFE_SSL_POLICY_VALUES
        ):
            return c_id
    return None


def tfm_lb_target_group_insecure_port(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_LB_TARGET_INSECURE_PORT

    def n_ids() -> Iterable[GraphShardNode]:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
