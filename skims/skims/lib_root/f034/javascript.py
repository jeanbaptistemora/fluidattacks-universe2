from lib_root.f034.common import (
    weak_random,
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


def js_weak_random(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_WEAK_RANDOM

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in weak_random(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f034.javascript_insecure_randoms.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
