from lib_root.f009.common import (
    crypto_credentials,
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


def js_crypto_js_credentials(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in crypto_credentials(graph=graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f009.crypto_js_credentials.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_CRYPTO_CREDENTIALS,
    )
