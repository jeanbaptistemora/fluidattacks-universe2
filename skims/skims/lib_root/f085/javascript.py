from collections.abc import (
    Iterator,
)
from lib_root.f085.common import (
    client_storage,
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


def javascript_client_storage(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_CLIENT_STORAGE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in client_storage(graph, method):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f085.client_storage.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
