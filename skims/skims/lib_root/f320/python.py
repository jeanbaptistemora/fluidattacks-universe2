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


def get_eval_danger(
    graph: Graph, n_id: NId, danger_set: set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def is_danger_auth(graph: Graph, n_id: NId) -> bool:
    args_ids = g.adj_ast(graph, n_id)
    # Only if no password, or password is a literal or None it is deterministic
    if len(args_ids) < 2:
        return True
    n_attrs = graph.nodes[args_ids[1]]
    return n_attrs["label_type"] == "Literal" or n_attrs.get("value") == "None"


def python_unsafe_ldap_connection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_LDAP_CONN_AUTH
    danger_set = {"simple_bind", "simple_bind_s", "bind", "bind_s"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(graph, label_type="MemberAccess"):
                n_attrs = graph.nodes[n_id]
                parent_id = g.pred_ast(graph, n_id)[0]
                if (
                    n_attrs["member"] in danger_set
                    and (al_id := graph.nodes[parent_id].get("arguments_id"))
                    and is_danger_auth(graph, al_id)
                    and get_eval_danger(
                        graph,
                        n_attrs["expression_id"],
                        {"ldapconnect"},
                        method,
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
