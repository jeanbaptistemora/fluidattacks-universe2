from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
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


def trust_boundary_violation(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_TRUST_BOUNDARY_VIOLATION
    danger_methods = {"setAttribute", "putValue"}
    danger_set = {"userparameters", "userconnection"}

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
                    and graph.nodes[obj_id].get("expression") == "getSession"
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and get_node_evaluation_results(
                        method, graph, al_id, danger_set
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f089.trust_boundary_violation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
