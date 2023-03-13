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


def ldap_injection(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_INJECTION
    danger_methods = {"FindOne", "FindAll"}
    danger_params = {"directorysearcher", "userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                expr = graph.nodes[n_id]["expression"].split(".")
                if expr[-1] in danger_methods and get_node_evaluation_results(
                    method,
                    graph,
                    n_id,
                    danger_params,
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
