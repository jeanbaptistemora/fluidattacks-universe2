from lib_root.f338.common import (
    has_dangerous_param,
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


def kotlin_salting_is_harcoded(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KOTLIN_SALT_IS_HARDCODED

    def n_ids() -> Iterable[GraphShardNode]:
        yield from (
            (shard, n_id)
            for shard in graph_db.shards_by_language(
                GraphLanguage.KOTLIN,
            )
            if shard.syntax_graph
            for n_id in has_dangerous_param(shard.syntax_graph, method)
        )

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f338.salt_is_hardcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
