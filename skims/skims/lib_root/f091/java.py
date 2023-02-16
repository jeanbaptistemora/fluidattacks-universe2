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


def is_logger_unsafe(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.JAVA_INSECURE_LOGGING
    if test_node := graph.nodes[n_id].get("arguments_id"):
        for path in get_backward_paths(graph, test_node):
            evaluation = evaluate(method, graph, path, test_node)
            if (
                evaluation
                and evaluation.danger
                and "userparams" in evaluation.triggers
                and not (
                    "sanitized" in evaluation.triggers
                    and "characters" in evaluation.triggers
                )
            ):
                return True

    return False


def insecure_logging(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_LOGGING
    danger_methods = {"logger.info", "log.debug", "log.info"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if m_name.lower() in danger_methods and is_logger_unsafe(
                    graph, m_id
                ):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
