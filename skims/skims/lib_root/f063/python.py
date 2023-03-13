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


def is_danger_attachment(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    args_ids = g.adj_ast(graph, n_id)
    if len(args_ids) < 2:
        return False

    for _id in args_ids[1:]:
        n_attrs = graph.nodes[_id]
        if n_attrs["label_type"] != "NamedArgument":
            continue
        if n_attrs["argument_name"] != "as_attachment":
            continue
        val_id = n_attrs["value_id"]
        return get_node_evaluation_results(method, graph, val_id, set())
    return False


def python_io_path_traversal(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_IO_PATH_TRAVERSAL

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.PYTHON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] == "send_file"
                    and (al_id := n_attrs.get("arguments_id"))
                    and is_danger_attachment(graph, al_id, method)
                    and get_node_evaluation_results(
                        method, graph, al_id, {"userparams"}
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f063_path_traversal.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
