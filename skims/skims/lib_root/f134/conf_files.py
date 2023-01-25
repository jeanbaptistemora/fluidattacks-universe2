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
            key_id = graph.nodes[parent_id]["key_id"]
            key = graph.nodes[key_id]["value"]
            if key == "http":
                return True
    return False


def get_value(graph: Graph, nid: NId) -> str:
    value = graph.nodes[nid]["value"] if graph.nodes[nid].get("value") else ""
    return value


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
                key_id = graph.nodes[nid]["key_id"]
                key = graph.nodes[key_id]["value"]
                value_id = graph.nodes[nid]["value_id"]
                value = get_value(graph, value_id)

                if is_in_path(graph, nid, key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f134.cfn_wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
