from lib_root.f344.common import (
    local_storage_from_assignment,
    local_storage_from_http,
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


def ts_local_storage_with_sensitive_data(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.TS_LOCAL_STORAGE_WITH_SENSITIVE_DATA

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in local_storage_from_http(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_LOCAL_STORAGE_WITH_SENSITIVE_DATA,
    )


def ts_local_storage_sens_data_assignment(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_LOCAL_STORAGE_SENS_DATA_ASSIGNMENT

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in local_storage_from_assignment(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
