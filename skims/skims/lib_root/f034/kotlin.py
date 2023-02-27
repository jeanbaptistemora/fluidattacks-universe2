from collections.abc import (
    Iterator,
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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        if evaluate(method, graph, path, n_id):
            return True
    return False


def weak_random(graph: Graph, method: MethodsEnum) -> Iterator[NId]:
    for n_id in g.matching_nodes(
        graph,
        label_type="MethodInvocation",
    ):
        if (
            "SecureRandom" in graph.nodes[n_id]["expression"]
            and (ar_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, ar_id).get("__0__"))
            and get_eval_danger(graph, test_node, method)
        ):
            yield n_id
        elif (
            "setSeed" in graph.nodes[n_id]["expression"]
            and (ar_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, ar_id).get("__0__"))
            and get_eval_danger(graph, test_node, method)
        ):
            yield test_node


def kt_weak_random(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_WEAK_RANDOM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.KOTLIN,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in weak_random(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f034.kt_weak_random.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
