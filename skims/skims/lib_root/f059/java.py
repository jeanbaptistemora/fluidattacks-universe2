from collections.abc import (
    Iterator,
)
from lib_root.utilities.java import (
    yield_method_invocation_syntax_graph,
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


def sensitive_log_info(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_SENSITIVE_INFO_IN_LOGS
    danger_methods = {"logger.info", "log.debug", "log.info"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if (
                    m_name.lower() in danger_methods
                    and (al_id := graph.nodes[m_id].get("arguments_id"))
                    and get_node_evaluation_results(
                        method, graph, al_id, {"sensitiveinfo"}
                    )
                ):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f059.java_sensitive_info_logs",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
