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


def _ec2_monitoring_disabled(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "monitoring"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() in {"false", "0"}:
                return b_id
    if not has_attr:
        return nid
    return None


def _distribution_has_logging_disabled(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "logging_config"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[b_id].get("name")
        if name == expected_attr:
            has_attr = True
    if not has_attr:
        return nid
    return None


def _trails_not_multiregion(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "is_multi_region_trail"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() not in {"true", "1"}:
                return b_id
    if not has_attr:
        return nid
    return None


def _elb_logging_disabled(graph: Graph, nid: NId) -> Optional[NId]:
    expected_block = "access_logs"
    expected_block_attr = "enabled"
    has_block = False
    for c_id in adj_ast(graph, nid, name=expected_block):
        has_block = True
        for b_id in adj_ast(graph, c_id, label_type="Pair"):
            key, value = get_key_value(graph, b_id)
            if key == expected_block_attr:
                if value.lower() == "false":
                    return b_id
                return None
    if not has_block:
        return nid
    return None


def _lambda_tracing_disabled(graph: Graph, nid: NId) -> Optional[NId]:
    expected_block = "tracing_config"
    expected_block_attr = "mode"
    has_block = False
    for c_id in adj_ast(graph, nid, name=expected_block):
        has_block = True
        for b_id in adj_ast(graph, c_id, label_type="Pair"):
            key, value = get_key_value(graph, b_id)
            if key == expected_block_attr and value != "Active":
                return b_id
            return None
    if not has_block:
        return nid
    return None


def tfm_lambda_tracing_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_LAMBDA_TRACING_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lambda_function"):
                if report := _lambda_tracing_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.tfm_lambda_func_has_trace_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_elb_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB_LOGGING_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_elb"):
                if report := _elb_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_trails_not_multiregion(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_TRAILS_NOT_MULTIREGION

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_cloudtrail"):
                if report := _trails_not_multiregion(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.trails_not_multiregion",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_distribution_has_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CF_DISTR_LOG_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_cloudfront_distribution"):
                if report := _distribution_has_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.tfm_has_logging_config_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_monitoring_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_MONITORING_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                if report := _ec2_monitoring_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.has_monitoring_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
