from lib_root.f042.common import (
    is_insecure_cookie,
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


def insecurely_generated_cookies(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSEC_COOKIES

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in is_insecure_cookie(graph, method):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f042.java_insecure_set_cookies.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
