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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_forward_paths,
)
from utils import (
    graph as g,
)


def eval_danger(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.JAVA_UPLOAD_SIZE_LIMIT
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def no_size_limit(graph: Graph, parent: str, var_name: str) -> bool:
    for path in get_forward_paths(graph, parent):
        for n_id in g.filter_nodes(
            graph,
            nodes=path,
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] == "setMaxUploadSize"
                and (symbol_id := n_attrs.get("object_id"))
                and graph.nodes[symbol_id]["symbol"] == var_name
            ):
                return eval_danger(graph, n_id)
    return True


def get_vuln_nodes(graph: Graph) -> list[str]:
    danger_objs = {"CommonsMultipartResolver", "MultipartConfigFactory"}
    vuln_nodes: list[str] = []
    for n_id in g.matching_nodes(graph, label_type="ObjectCreation"):
        n_name = graph.nodes[n_id].get("name")

        if n_name in danger_objs:
            parent = g.pred_ast(graph, n_id)[0]
            var_name = graph.nodes[parent].get("variable")
            if no_size_limit(graph, parent, var_name):
                vuln_nodes.append(parent)
    return vuln_nodes


def insecure_file_upload_size(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:

        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in get_vuln_nodes(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f354.java_upload_size_limit",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_UPLOAD_SIZE_LIMIT,
    )
