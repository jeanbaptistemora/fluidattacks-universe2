from collections.abc import (
    Iterator,
)
from lib_root.f297.common import (
    get_vuln_nodes,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def sql_injection(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    typescript = GraphLanguage.TYPESCRIPT
    method = MethodsEnum.TS_SQL_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(typescript):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in get_vuln_nodes(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f297.sql_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
