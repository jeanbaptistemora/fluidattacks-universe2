from lib_root.f338.common import (
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
from typing import (
    Iterable,
)


def js_salting_is_harcoded(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_SALT_IS_HARDCODED

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
        desc_key="src.lib_root.f280.non_secure_construction_of_cookies",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
