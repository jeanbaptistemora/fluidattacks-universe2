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
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def have_insecure_http_server(graph: Graph, nid: NId) -> Tuple[bool, NId]:
    required_flags = {" -S", " --tls", " --ssl"}
    c_ids = adj_ast(graph, nid)
    for c_id in c_ids:
        value_id = graph.nodes[c_id]["value_id"]
        value = graph.nodes[value_id].get("value")
        if (
            value
            and "http-server" in value
            and not any(flag in value for flag in required_flags)
        ):
            return True, c_id
    return False, ""


def https_flag_missing(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_HTTPS_FLAG_MISSING

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key_id = graph.nodes[nid]["key_id"]
                key = graph.nodes[key_id]["value"]
                value_id = graph.nodes[nid]["value_id"]

                if (
                    key == "scripts"
                    and (result := have_insecure_http_server(graph, value_id))
                    and result[0]
                ):
                    yield shard, result[1]

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f372.json_https_flag_missing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
