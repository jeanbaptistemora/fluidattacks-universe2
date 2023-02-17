from collections.abc import (
    Iterator,
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


def _ec2_monitoring_disabled(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "monitoring")
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
    return None


def _distribution_has_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    block = get_argument(graph, nid, "logging_config")
    if not block:
        return nid
    return None


def _trails_not_multiregion(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "is_multi_region_trail"
    )
    if not attr:
        return nid
    if attr_val.lower() not in {"true", "1"}:
        return attr_id
    return None


def _elb_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    access = get_argument(graph, nid, "access_logs")
    if not access:
        return nid
    attr, attr_val, attr_id = get_attribute(graph, access, "enabled")
    if attr and attr_val.lower() == "false":
        return attr_id
    return None


def _lambda_tracing_disabled(graph: Graph, nid: NId) -> NId | None:
    tracing = get_argument(graph, nid, "tracing_config")
    if not tracing:
        return nid
    attr, attr_val, attr_id = get_attribute(graph, tracing, "mode")
    if attr and attr_val != "Active":
        return attr_id
    return None


def tfm_lambda_tracing_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_LAMBDA_TRACING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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

    def n_ids() -> Iterator[GraphShardNode]:
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
