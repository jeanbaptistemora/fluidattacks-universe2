from collections.abc import (
    Iterator,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def remote_command_execution(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_REMOTE_COMMAND_EXECUTION
    danger_p1 = {"UserConnection", "UserParams"}
    danger_p2 = {"Executor", "UserConnection", "UserParams"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(
                graph, {"Start", "Execute"}
            ):
                check = graph.nodes[n_id]["expression"].split(".")[-1].lower()
                if (
                    check == "start"
                    and get_node_evaluation_results(
                        method, graph, n_id, danger_p1, False
                    )
                ) or (
                    check == "execute"
                    and get_node_evaluation_results(
                        method, graph, n_id, danger_p2, False
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
