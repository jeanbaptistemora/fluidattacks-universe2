from lib_root.f008.common import (
    is_argument_vuln,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
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
from typing import (
    Iterable,
)


def reflected_xss(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    typescript = GraphLanguage.TYPESCRIPT
    method = MethodsEnum.TS_REFLECTED_XSS
    danger_methods = {"send"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(typescript):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if is_argument_vuln(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
