from collections.abc import (
    Iterator,
)
from lib_root.f008.common import (
    unsafe_xss_content_nodes,
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


def unsafe_xss_content(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    typescript = GraphLanguage.TYPESCRIPT
    method = MethodsEnum.TS_UNSAFE_XSS_CONTENT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(typescript):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in unsafe_xss_content_nodes(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
