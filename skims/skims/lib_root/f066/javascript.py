from lib_root.f066.common import (
    nid_uses_console_log,
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


def js_uses_console_log(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_CONSOLE_LOG

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in nid_uses_console_log(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.generic_uses_console_log",
        desc_params=dict(lang="Javascript"),
        graph_shard_nodes=n_ids(),
        method=method,
    )
