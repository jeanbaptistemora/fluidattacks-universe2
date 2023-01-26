from lib_root.utilities.json import (
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, nid: NId, key_pair: str, value: str) -> bool:
    correct_parents = ["iisSettings"]
    if (
        key_pair == "anonymousAuthentication"
        and value == "true"
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def get_value(graph: Graph, nid: NId) -> str:
    value = graph.nodes[nid]["value"] if graph.nodes[nid].get("value") else ""
    return value


def anon_connection_config(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_ANON_CONNECTION_CONFIG

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
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
        desc_key="lib_root.f056.json_anon_connection_config",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
