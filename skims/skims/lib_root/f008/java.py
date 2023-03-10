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
from utils import (
    graph as g,
)


def is_xss_content_creation(
    method: MethodsEnum,
    graph: Graph,
    method_id: NId,
    obj_id: NId,
) -> bool:
    danger_set1 = {"userconnection", "userparameters"}
    danger_set2 = {"userresponse"}
    al_id = graph.nodes[method_id].get("arguments_id")
    response_id = graph.nodes[obj_id].get("object_id")
    if not (al_id and response_id):
        return False

    if get_node_evaluation_results(
        method, graph, al_id, danger_set1, False
    ) and get_node_evaluation_results(
        method, graph, response_id, danger_set2, False
    ):
        return True
    return False


def unsafe_xss_content(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_UNSAFE_XSS_CONTENT
    danger_methods = {"format", "write", "println", "printf", "print"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (obj_id := n_attrs.get("object_id"))
                    and graph.nodes[obj_id].get("expression") == "getWriter"
                    and is_xss_content_creation(method, graph, n_id, obj_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
