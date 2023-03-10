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


def kt_weak_random(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_WEAK_RANDOM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                expr = graph.nodes[n_id]["expression"].split(".")[-1]
                if (
                    expr in {"SecureRandom", "setSeed"}
                    and (ar_id := graph.nodes[n_id].get("arguments_id"))
                    and (test_node := g.match_ast(graph, ar_id).get("__0__"))
                    and get_node_evaluation_results(
                        method, graph, test_node, set()
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f034.kt_weak_random.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
