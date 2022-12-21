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


def is_ldap_injection(
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


def ldap_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_INJECTION
    csharp = GraphShardMetadataLanguage.CSHARP
    danger_methods = {"FindOne", "FindAll"}
    danger_params = {"directorysearcher", "userparameters", "userconnection"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(csharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                expr = graph.nodes[n_id]["expression"].split(".")
                if expr[-1] in danger_methods and is_ldap_injection(
                    graph, n_id, danger_params, method
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
