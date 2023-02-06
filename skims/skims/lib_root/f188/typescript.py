from lib_root.f188.common import (
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


def lack_of_validation_dom_window(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TSX_LACK_OF_VALIDATION_EVENT_LISTENER

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in has_dangerous_param(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f188.lack_of_data_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
