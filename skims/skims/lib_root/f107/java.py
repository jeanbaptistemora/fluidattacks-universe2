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
    method = MethodsEnum.JAVA_LDAP_INJECTION
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                expr = graph.nodes[n_id]["expression"].split(".")
                pred = g.pred(graph, n_id)[0]
                var_type = graph.nodes[pred].get("variable_type")
                if (
                    expr[-1] == "search"
                    and "NamingEnumeration" in var_type
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__1__"))
                    and get_node_evaluation_results(
                        method, graph, arg_id, danger_set
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
