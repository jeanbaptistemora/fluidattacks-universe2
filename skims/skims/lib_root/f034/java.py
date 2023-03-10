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


def get_eval_results(
    method: MethodsEnum, graph: Graph, n_id: NId, danger_stmt: str
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and danger_stmt in evaluation.triggers:
            return True
    return False


def is_attribute_weak(
    method: MethodsEnum, graph: Graph, obj_id: NId, al_id: NId
) -> bool:
    args_ids = g.adj_ast(graph, al_id)
    if (
        len(args_ids) >= 2
        and graph.nodes[args_ids[0]].get("symbol") == "cookieName"
        and get_eval_results(method, graph, obj_id, "userrequest")
        and get_eval_results(method, graph, args_ids[1], "weakrandom")
    ):
        return True

    return False


def is_weak_random(
    method: MethodsEnum, graph: Graph, obj_id: NId, al_id: NId
) -> bool:
    if graph.nodes[obj_id].get("expression") == "getSession":
        return is_attribute_weak(method, graph, obj_id, al_id)

    if (
        (args_ids := g.adj_ast(graph, al_id))
        and len(args_ids) == 1
        and get_eval_results(method, graph, obj_id, "userresponse")
    ):
        return get_eval_results(method, graph, args_ids[0], "weakrandom")

    return False


def java_weak_random(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_WEAK_RANDOM_COOKIE
    danger_methods = {"setAttribute", "addCookie"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_attrs = graph.nodes[n_id]
                expr = n_attrs["expression"].split(".")
                if (
                    expr[-1] in danger_methods
                    and (obj_id := n_attrs.get("object_id"))
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and is_weak_random(method, graph, obj_id, al_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f034.java_use_insecure_randms.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
