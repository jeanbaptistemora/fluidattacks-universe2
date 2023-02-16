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
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_lambda_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    block_id = graph.nodes[n_id]["block_id"]
    n_attrs = graph.nodes[block_id]
    test_nid = block_id
    if n_attrs["label_type"] == "ExecutionBlock" and (
        test_id := g.match_ast_d(graph, block_id, "Return")
    ):
        return get_eval_danger(graph, test_id, method)

    return get_eval_danger(graph, test_nid, method)


def is_validation_dangerous(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    parent_id = g.pred(graph, n_id)[0]
    if graph.nodes[parent_id]["label_type"] == "Assignment":
        assign_id = g.adj_ast(graph, parent_id)[1]
        label_type = graph.nodes[assign_id]["label_type"]
        if label_type == "LambdaExpression" and is_lambda_danger(
            graph, assign_id, method
        ):
            return True
    return False


def insecure_certificate_validation(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    method = MethodsEnum.CS_INSECURE_CERTIFICATE_VALIDATION
    danger_m = "ServerCertificateValidationCallback"

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                if graph.nodes[nid].get(
                    "member"
                ) == danger_m and is_validation_dangerous(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.insecure_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
