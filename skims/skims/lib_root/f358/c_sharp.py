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


def get_eval_triggers(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    danger_triggers = {"return_true"}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger_triggers:
            return True
    return False


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> list[NId]:
    nodes = graph.nodes
    for n_id in g.matching_nodes(
        graph,
        label_type="MemberAccess",
        expression="ServicePointManager",
        member="ServerCertificateValidationCallback",
    ):
        vuln_nodes: list[NId] = []
        if (
            (parent_n_id := next(iter(g.pred_ast(graph, n_id)), None))
            and (nodes[parent_n_id].get("label_type") == "Assignment")
            and (sibling_n_id := nodes[parent_n_id].get("value_id"))
            and (get_eval_triggers(graph, sibling_n_id, method))
        ):
            vuln_nodes.append(sibling_n_id)

    return vuln_nodes


def cert_validation_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_CERT_VALIDATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in get_vuln_nodes(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f358.csharp_cert_validation_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
