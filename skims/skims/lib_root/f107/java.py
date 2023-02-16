from collections.abc import (
    Iterator,
    Set,
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
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_LDAP_INJECTION
    java = GraphShardMetadataLanguage.JAVA
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
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
                    and is_ldap_injection(graph, arg_id, danger_set, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
