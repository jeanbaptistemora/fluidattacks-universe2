from lib_root.f353.common import (
    insecure_jwt_decode,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)


def decode_insecure_jwt_token(
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_DECODE_INSECURE_JWT_TOKEN

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in insecure_jwt_decode(graph):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f353.js_decode_insecure_jwt_token",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
