from lib_root.f128.common import (
    insecure_cookies,
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


def typescript_insecure_cookies(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_COOKIE

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in insecure_cookies(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f135.ts_unsafe_http_xss_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
