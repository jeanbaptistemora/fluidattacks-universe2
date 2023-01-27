from lib_root.utilities.json import (
    get_value,
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


def correct_email(value: str) -> bool:
    regex_email = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex_email, value):
        return True
    return False


def _sensitive_info_in_dotnet(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    correct_parents = ["OutlookServices"]
    if (
        key_pair == "Email"
        and correct_email(value)
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def _sensitive_info_json(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    correct_parents = ["ConnectionStrings"]
    if (
        key_pair == "Claims"
        and has_password(value)
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def _sensitive_key_in_json(key_pair: str, value: str) -> bool:
    key_smell = {
        "api_key",
        "current_key",
    }
    grammar = re.compile(r"[A-Za-z0-9]{5,}")
    if key_pair in key_smell and re.fullmatch(grammar, value):
        return True
    return False


def sensitive_key_in_json(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_KEY_JSON

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

                if _sensitive_key_in_json(key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f009.sensitive_key_in_json.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def sensitive_info_in_dotnet(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_INFO_DOTNET_JSON

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

                if _sensitive_info_in_dotnet(graph, nid, key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f009.sensitive_key_in_json.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def sensitive_info_json(
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

                if _sensitive_info_json(graph, nid, key, value):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f009.sensitive_key_in_json.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
