from lib_root.utilities.json import (
    is_parent,
    list_has_string,
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


def has_wildcard(graph: Graph, nid: NId, key_dict: str, value_id: NId) -> bool:
    correct_parents = [
        "CorsRules",
        "CorsConfiguration",
        "Properties",
        "S3Bucket",
    ]
    if key_dict == "AllowedOrigins" and is_parent(graph, nid, correct_parents):
        if graph.nodes[value_id]["label_type"] == "Literal":
            value = graph.nodes[value_id]["value"]
            if value == "*":
                return True
        if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
            if list_has_string(graph, value_id, "*"):
                return True
    return False


def wildcard_in_allowed_origins(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_WILDCARD_IN_ALLOWED_ORIGINS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key_id = graph.nodes[nid]["key_id"]
                key = graph.nodes[key_id]["value"]
                value_id = graph.nodes[nid]["value_id"]

                if has_wildcard(graph, nid, key, value_id):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f134.cfn_wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
