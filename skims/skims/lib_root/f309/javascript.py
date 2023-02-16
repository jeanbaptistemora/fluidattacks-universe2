from collections.abc import (
    Iterator,
)
from lib_root.f309.common import (
    is_insecure_jwt,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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


def uses_insecure_jwt_token(
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_INSECURE_JWT_TOKEN
    jwt_methods = {"sign", "verify"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in yield_syntax_graph_member_access(graph, jwt_methods):
                if is_insecure_jwt(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f309.js_uses_insecure_jwt_token",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
