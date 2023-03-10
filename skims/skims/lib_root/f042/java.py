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
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_unsafe_cookie(
    method: MethodsEnum, graph: Graph, n_id: NId, cookie_name: str
) -> bool:
    for path in get_backward_paths(graph, n_id):
        for node in path:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["label_type"] == "MethodInvocation"
                and n_attrs["expression"] == "setSecure"
                and (al_id := n_attrs.get("arguments_id"))
                and (obj_id := n_attrs.get("object_id"))
                and graph.nodes[obj_id].get("symbol") == cookie_name
            ):
                return get_node_evaluation_results(method, graph, al_id, set())
    return False


def analyze_insecure_cookie(
    method: MethodsEnum, graph: Graph, obj_id: NId, al_id: NId
) -> bool:
    args_ids = g.adj_ast(graph, al_id)
    if (
        len(args_ids) == 1
        and get_node_evaluation_results(
            method, graph, obj_id, {"userresponse"}
        )
        and (cookie_name := graph.nodes[args_ids[0]].get("symbol"))
    ):
        return is_unsafe_cookie(method, graph, args_ids[0], cookie_name)
    return False


def java_insecure_cookie(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_COOKIE
    danger_methods = {"addCookie"}

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
                    and analyze_insecure_cookie(method, graph, obj_id, al_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f042.java_insecure_set_cookies.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
