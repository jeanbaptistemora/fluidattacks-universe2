from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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


def _bucket_has_logging_conf_disabled(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    log_config, _, _ = get_attribute(graph, val_id, "LoggingConfiguration")
    if not log_config:
        yield prop_id


def _cf_distribution_has_logging_disabled(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    dist_config, _, dist_config_id = get_attribute(
        graph, val_id, "DistributionConfig"
    )
    if dist_config:
        data_id = graph.nodes[dist_config_id]["value_id"]
        logging, _, _ = get_attribute(graph, data_id, "Logging")
        if not logging:
            yield dist_config_id


def cfn_cf_distribution_has_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_CF_DISTR_LOG_DISABLED

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
                for report in _cf_distribution_has_logging_disabled(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_bucket_has_logging_conf_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_LOG_CONF_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::S3::Bucket"):
                for report in _bucket_has_logging_conf_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.bucket_has_logging_conf_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
