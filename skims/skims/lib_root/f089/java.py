from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
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


def is_trust_violation(
    graph: Graph, nid: NId, danger_set: Set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, nid):
        evaluation = evaluate(method, graph, path, nid)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def trust_boundary_violation(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_TRUST_BOUNDARY_VIOLATION
    java = GraphShardMetadataLanguage.JAVA
    danger_methods = {"setAttribute", "putValue"}
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
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
                    and is_trust_violation(graph, al_id, danger_set, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f089.trust_boundary_violation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
