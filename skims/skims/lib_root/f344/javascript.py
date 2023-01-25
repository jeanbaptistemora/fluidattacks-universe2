from lib_root.f344.common import (
    local_storage_from_async,
    local_storage_from_callback,
    local_storage_from_http,
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


def js_local_storage_with_sensitive_data(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
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
        method=MethodsEnum.JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA,
    )


def js_local_storage_sens_data_async(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_ASYNC

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in local_storage_from_async(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_ASYNC,
    )


def js_local_storage_sens_data_callback(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_CALLBACK

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in local_storage_from_callback(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_CALLBACK,
    )
