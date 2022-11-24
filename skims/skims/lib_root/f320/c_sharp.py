from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
)
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_node_danger(graph: Graph, nid: NId) -> bool:
    method = MethodsEnum.CS_LDAP_CONN_AUTH
    var = {graph.nodes[g.pred(graph, nid)[0]].get("variable")}

    if set(yield_syntax_graph_member_access(graph, var)):
        return False

    args_nid = graph.nodes[nid].get("arguments_id")
    test_nid = g.adj_ast(graph, args_nid)[3]

    for path in get_backward_paths(graph, test_nid):
        evaluation = evaluate(method, graph, path, test_nid)
        if evaluation and evaluation.danger:
            return True
    return False


def ldap_connections_authenticated(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_CONN_AUTH

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in yield_syntax_graph_object_creation(
                graph, {"DirectoryEntry"}
            ):
                if is_node_danger(graph, nid):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
