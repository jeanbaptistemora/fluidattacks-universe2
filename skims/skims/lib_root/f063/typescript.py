from lib_root.f063.common import (
    get_eval_danger,
    insecure_path_traversal,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def typescript_insecure_path_traversal(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_PATH_TRAVERSAL

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in insecure_path_traversal(graph, method):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.js_insecure_path_traversal",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def zip_slip_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_ZIP_SLIP
    danger_methods = {"createWriteStream"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if get_eval_danger(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.js_insecure_path_traversal",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
