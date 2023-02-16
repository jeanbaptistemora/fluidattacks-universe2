from collections.abc import (
    Iterator,
)
from lib_root.f060.common import (
    has_dangerous_param,
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


def unsafe_origin(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_UNSAFE_ORIGIN

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
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
