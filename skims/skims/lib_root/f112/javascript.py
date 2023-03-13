from collections.abc import (
    Iterator,
)
from lib_root.f112.common import (
    sql_injection,
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


def unsafe_sql_injection(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JS_SQL_API_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVASCRIPT):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in sql_injection(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.F112.user_controled_param",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
