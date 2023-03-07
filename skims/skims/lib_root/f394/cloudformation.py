from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    TRUE_OPTIONS,
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


def _log_files_not_validated(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    file_validation, file_val, file_id = get_attribute(
        graph, val_id, "EnableLogFileValidation"
    )
    if not file_validation:
        yield prop_id
    elif file_val not in TRUE_OPTIONS:
        yield file_id


def cfn_log_files_not_validated(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_LOG_NOT_VALIDATED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::CloudTrail::Trail"):
                for report in _log_files_not_validated(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f394.cfn_log_files_not_validated",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
