from collections.abc import (
    Iterator,
    Set,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
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


def is_node_vuln(graph: Graph, n_id: NId, danger_set: Set[str]) -> bool:
    method = MethodsEnum.JAVA_UNSAFE_XSS_CONTENT
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger_set:
            return True
    return False


def is_xss_content_creation(
    graph: Graph,
    method_id: NId,
    obj_id: NId,
) -> bool:
    danger_connection = {"userconnection", "userparameters"}
    danger_response = {"userresponse"}
    al_id = graph.nodes[method_id].get("arguments_id")
    response_id = graph.nodes[obj_id].get("object_id")

    if not (al_id and response_id):
        return False

    if is_node_vuln(graph, al_id, danger_connection) and is_node_vuln(
        graph, response_id, danger_response
    ):
        return True

    return False


def unsafe_xss_content(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    java = GraphLanguage.JAVA
    danger_methods = {"format", "write", "println", "printf", "print"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (obj_id := n_attrs.get("object_id"))
                    and graph.nodes[obj_id].get("expression") == "getWriter"
                    and is_xss_content_creation(graph, n_id, obj_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_UNSAFE_XSS_CONTENT,
    )
