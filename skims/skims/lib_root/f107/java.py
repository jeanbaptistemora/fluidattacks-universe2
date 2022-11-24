from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
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
)
from utils import (
    graph as g,
)


def is_filter_insecure(graph: Graph, nid: NId) -> bool:
    method = core_model.MethodsEnum.JAVA_LDAP_INJECTION
    rules = {"UserParams", "HttpServletRequest"}
    for path in get_backward_paths(graph, nid):
        evaluation = evaluate(method, graph, path, nid)
        if evaluation and evaluation.triggers == rules:
            return True
    return False


def ldap_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    java = GraphShardMetadataLanguage.JAVA
    ldap_var = "NamingEnumeration"

    def n_ids() -> Iterable[GraphShardNode]:

        for shard in graph_db.shards_by_language(java):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, {"search"}):
                pred = g.pred(graph, nid)[0]
                if ldap_var in graph.nodes[pred].get("variable_type") and (
                    (args_id := graph.nodes[nid].get("arguments_id"))
                    and (test_nid := g.match_ast(graph, args_id).get("__1__"))
                    and is_filter_insecure(graph, test_nid)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JAVA_LDAP_INJECTION,
    )
