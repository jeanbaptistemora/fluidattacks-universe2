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


def _api_gateway_access_logging_disabled(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    access_settings, _, _ = get_attribute(graph, val_id, "AccessLogSetting")
    if not access_settings:
        yield prop_id


def cfn_api_gateway_access_logging_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_API_GATEWAY_LOGGING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::ApiGateway::Stage"):
                for report in _api_gateway_access_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f408.cfn_has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
