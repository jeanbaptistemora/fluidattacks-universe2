from lib_root.f060.common import (
    has_dangerous_param,
)
from lib_sast.types import (
    ShardDb,
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


def unsafe_origin(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_UNSAFE_ORIGIN

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in has_dangerous_param(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.common_unsafe_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
