from lib_root.utilities.json import (
    get_key_value,
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, nid: NId, key_dict: str, value: str) -> bool:
    last_nid = nid
    if key_dict == "cors" and value == "true":
        parent = g.search_pred_until_type(graph, last_nid, {"Pair"})
        if parent_id := parent[0] if parent != ("", "") else None:
            key, _ = get_key_value(graph, parent_id)
            if key == "http":
                return True
    return False


def serverles_cors_true(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.YML_SERVERLES_CORS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key, value = get_key_value(graph, nid)

                if is_in_path(graph, nid, key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f134.cfn_wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
