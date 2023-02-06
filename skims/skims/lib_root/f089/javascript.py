from lib_root.f089.common import (
    json_parse_unval_data,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)


def json_parse_unvalidated_data(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_JSON_PARSE_UNVALIDATED_DATA

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in json_parse_unval_data(graph):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f089.trust_boundary_violation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
