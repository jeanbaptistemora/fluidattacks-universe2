from collections.abc import (
    Iterator,
)
from lib_root.utilities.json import (
    get_key_value,
    is_parent,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def _sourcemap_enabled(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    if key_pair == "sourceMap" and value.lower() == "true":
        tsconfig_correct_parents = ["compilerOptions"]
        angular_vuln_parents_path = ["production", "configurations", "build"]
        if is_parent(graph, nid, tsconfig_correct_parents):
            return True
        if is_parent(graph, nid, angular_vuln_parents_path):
            return True
    if key_pair == "sourceMaps" and value.lower() == "true":
        serverless_correct_parents = ["configurations"]
        if is_parent(graph, nid, serverless_correct_parents):
            return True
    return False


def tsconfig_sourcemap_enabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TSCONFIG_SOURCEMAP_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None or shard.path.endswith(
                "tsconfig.spec.json"
            ):
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key, value = get_key_value(graph, nid)

                if _sourcemap_enabled(graph, nid, key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f236.tsconfig_sourcemap_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
