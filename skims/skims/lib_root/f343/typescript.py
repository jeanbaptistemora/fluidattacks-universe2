from lib_root.f343.common import (
    webpack_insecure_compression,
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


def ts_insecure_compression(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.TS_INSECURE_COMPRESSION_ALGORITHM

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in webpack_insecure_compression(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f343.insecure_compression_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_INSECURE_COMPRESSION_ALGORITHM,
    )
