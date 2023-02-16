from collections.abc import (
    Iterator,
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
from symbolic_eval.utils import (
    get_object_identifiers,
    get_value_member_access,
)


def disabled_http_header_check(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_HTTP_HEADER_CHECK
    c_sharp = GraphLanguage.CSHARP
    http_obj = {"HttpRuntimeSection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for ident in get_object_identifiers(graph, http_obj):
                if (
                    value := get_value_member_access(
                        graph, ident, "EnableHeaderChecking"
                    )
                ) and graph.nodes[value].get("value") == "false":
                    yield shard, value

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f414.disabled_http_header_check",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
