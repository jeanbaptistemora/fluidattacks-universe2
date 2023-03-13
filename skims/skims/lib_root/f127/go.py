from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def go_insecure_query_float(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.GO_INSECURE_QUERY_FLOAT
    danger_methods = {
        "Exec",
        "ExecContext",
        "Query",
        "QueryContext",
        "QueryRow",
        "QueryRowContext",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                m_name = graph.nodes[n_id]["expression"].split(".")
                if (
                    m_name[-1] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and get_node_evaluation_results(
                        method, graph, al_id, {"userconnection"}
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="F127.title",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
