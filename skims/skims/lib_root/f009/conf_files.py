from lib_sast.types import (
    ShardDb,
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
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def has_password(value: str) -> bool:
    regex_password = re.compile(r"Password=.*")
    for element in value.split(";"):
        if re.match(regex_password, element):
            return True
    return False


def is_in_path(graph: Graph, nid: NId, key_pair: str, value: str) -> bool:
    correct_parents = ["ConnectionStrings"]
    last_nid = nid
    if key_pair == "Claims" and has_password(value):
        for correct_parent in correct_parents:
            parent = g.search_pred_until_type(graph, last_nid, {"Pair"})
            parent_id = parent[0] if parent != ("", "") else None
            if parent_id:
                key_id = graph.nodes[parent_id]["key_id"]
                key = graph.nodes[key_id]["value"]
                if key == correct_parent:
                    last_nid = parent_id
                    continue
                return False
            return False
        return True
    return False


def get_value(graph: Graph, nid: NId) -> str:
    value = graph.nodes[nid]["value"] if graph.nodes[nid].get("value") else ""
    return value


def sensitive_info_json(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_INFO_JSON

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
        desc_key="src.lib_path.f009.sensitive_key_in_json.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )