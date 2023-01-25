from lib_root.f091.common import (
    insecure_logging,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
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


def typescript_insecure_logging(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_LOGGING

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id in insecure_logging(graph, method):
                yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
