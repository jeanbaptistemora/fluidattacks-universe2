from lib_root.utilities.java import (
    yield_method_invocation_syntax_graph,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Iterable,
)


def is_log_sensitive(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.JAVA_SENSITIVE_INFO_IN_LOGS
    if test_node := graph.nodes[n_id].get("arguments_id"):
        for path in get_backward_paths(graph, test_node):
            evaluation = evaluate(method, graph, path, test_node)
            if (
                evaluation
                and evaluation.danger
                and "sensitiveinfo" in evaluation.triggers
            ):
                return True

    return False


def sensitive_log_info(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_SENSITIVE_INFO_IN_LOGS
    danger_methods = {"logger.info", "log.debug", "log.info"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if m_name.lower() in danger_methods and is_log_sensitive(
                    graph, m_id
                ):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f059.java_sensitive_info_logs",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
