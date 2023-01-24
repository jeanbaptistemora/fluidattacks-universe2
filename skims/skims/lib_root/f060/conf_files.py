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
    Iterator,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def has_insecure_flag(graph: Graph, nid: NId, key: str) -> Iterator[NId]:
    if key == "scripts":
        c_ids = adj_ast(graph, nid)
        for c_id in c_ids:
            value_id = graph.nodes[c_id]["value_id"]
            value = graph.nodes[value_id].get("value")
            if value and " --disable-host-check" in value:
                yield c_id


def disable_host_check(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_DISABLE_HOST_CHECK

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Pair"):
                key_id = graph.nodes[nid]["key_id"]
                key = graph.nodes[key_id]["value"]
                value_id = graph.nodes[nid]["value_id"]
                result = has_insecure_flag(graph, value_id, key)
                for vuln in result:
                    yield shard, vuln

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.json_disable_host_check",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
