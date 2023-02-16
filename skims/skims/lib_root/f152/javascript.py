from collections.abc import (
    Iterator,
)
from lib_root.f152.common import (
    insecure_http_headers,
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


def javascript_insecure_header_xframe_options(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_UNSAFE_HTTP_X_FRAME_OPTIONS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in insecure_http_headers(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f152.ts_unsafe_http_xframe_options",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
