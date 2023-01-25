from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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
from typing import (
    Iterable,
    Set,
)
from utils import (
    graph as g,
)


def is_node_vuln(
    graph: Graph, n_id: NId, method: MethodsEnum, danger_set: Set[str]
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def open_redirect(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    method = MethodsEnum.CS_OPEN_REDIRECT

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"Response"}
            ):
                if (
                    graph.nodes[member].get("member") == "Redirect"
                    and (pred := g.pred_ast(graph, member)[0])
                    and is_node_vuln(graph, pred, method, set())
                ):
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.c_sharp_open_redirect",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def unsafe_path_traversal(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_UNSAFE_PATH_TRAVERSAL
    c_sharp = GraphLanguage.CSHARP
    danger_methods = {
        "File.Copy",
        "File.Create",
        "File.Delete",
        "File.Exists",
        "File.Move",
        "File.Open",
        "File.Replace",
    }
    danger_set = {"userconnection", "userparameters"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if is_node_vuln(graph, n_id, method, danger_set):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f063_path_traversal.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
