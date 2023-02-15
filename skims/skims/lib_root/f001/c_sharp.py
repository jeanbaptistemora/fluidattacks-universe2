from collections.abc import (
    Iterator,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def is_sql_injection(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    al_id = graph.nodes[n_id].get("arguments_id")
    if not al_id:
        return False
    test_nid = g.adj_ast(graph, al_id)[0]

    for path in get_backward_paths(graph, test_nid):
        evaluation = evaluate(method, graph, path, test_nid)
        if evaluation and evaluation.danger:
            return True

    return False


def is_execute_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    danger_methods = {
        "ExecuteNonQuery",
        "ExecuteScalar",
        "ExecuteOracleNonQuery",
        "ExecuteOracleScalar",
        "ExecuteNonQueryAsync",
        "ExecuteScalarAsync",
        "ExecuteReaderAsync",
    }
    danger_params = {"UserParams"}
    if graph.nodes[n_id].get("member") not in danger_methods:
        return False
    test_nid = graph.nodes[n_id].get("expression_id")
    for path in get_backward_paths(graph, test_nid):
        evaluation = evaluate(method, graph, path, test_nid)
        if evaluation and evaluation.triggers == danger_params:
            return True
    return False


def sql_injection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"ExecuteSqlCommand"}
    danger_objects = {"SqlCommand"}
    method = MethodsEnum.CS_SQL_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in [
                *search_method_invocation_naive(graph, danger_methods),
                *yield_syntax_graph_object_creation(graph, danger_objects),
            ]:
                if is_sql_injection(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.001.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def sql_user_params(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_UNSAFE_SQL_STATEMENT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                if is_execute_danger(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.F001.user_controled_param",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
