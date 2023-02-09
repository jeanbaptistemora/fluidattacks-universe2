from lib_root.f379.common import (
    import_is_not_used,
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


def ts_import_is_never_used(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_UNNECESSARY_IMPORTS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.graph
            for n_id in import_is_not_used(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f379.unnused_imports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
