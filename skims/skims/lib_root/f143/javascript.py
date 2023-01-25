from lib_root.f143.common import (
    has_eval,
    is_insec_invocation,
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


def uses_eval(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_EVAL

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in has_eval(graph):
                if is_insec_invocation(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f143.uses_eval",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
