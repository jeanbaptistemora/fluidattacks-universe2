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
    GraphShardMetadataLanguage,
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
from typing import (
    Iterable,
    Set,
)
from utils import (
    graph as g,
)


def get_eval_results(
    graph: Graph, n_id: NId, danger_set: Set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger_set:
            return True
    return False


def is_weak_random(
    graph: Graph, obj_id: NId, al_id: NId, method: MethodsEnum
) -> bool:
    args_ids = g.adj_ast(graph, al_id)
    if (
        len(args_ids) >= 2
        and graph.nodes[args_ids[0]].get("symbol") == "cookieName"
        and get_eval_results(graph, obj_id, {"userresponse"}, method)
        and get_eval_results(graph, args_ids[1], {"weakrandom"}, method)
    ):
        return True

    return False


def java_weak_random(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_WEAK_RANDOM_COOKIE
    java = GraphShardMetadataLanguage.JAVA
    danger_methods = {"setAttribute"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_attrs = graph.nodes[n_id]
                expr = n_attrs["expression"].split(".")
                if (
                    expr[-1] in danger_methods
                    and (obj_id := n_attrs.get("object_id"))
                    and graph.nodes[obj_id].get("expression") == "getSession"
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and is_weak_random(graph, obj_id, al_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f034.javascript_insecure_randoms.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
