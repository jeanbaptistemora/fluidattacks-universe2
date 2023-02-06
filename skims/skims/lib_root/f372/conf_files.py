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
    Iterator,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def have_insecure_http_server(
    graph: Graph, nid: NId, key: str
) -> Iterator[NId]:
    required_flags = {" -S", " --tls", " --ssl"}
    if key == "scripts":
        c_ids = adj_ast(graph, nid)
        for c_id in c_ids:
            value_id = graph.nodes[c_id]["value_id"]
            value = graph.nodes[value_id].get("value")
            if (
                value
                and "http-server" in value
                and not any(flag in value for flag in required_flags)
            ):
                yield c_id


def https_flag_missing(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_HTTPS_FLAG_MISSING

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key, _ = get_key_value(graph, nid)
                value_id = graph.nodes[nid]["value_id"]
                result = have_insecure_http_server(graph, value_id, key)
                for vuln in result:
                    yield shard, vuln

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f372.json_https_flag_missing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
