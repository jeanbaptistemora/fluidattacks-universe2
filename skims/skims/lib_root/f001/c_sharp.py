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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_sql_injection(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (args_ids := g.adj_ast(graph, al_id))
        and len(args_ids) > 0
        and get_node_evaluation_results(method, graph, args_ids[0], set())
    ):
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
    danger_set = {"UserParams"}
    if (
        graph.nodes[n_id].get("member") in danger_methods
        and (test_id := graph.nodes[n_id].get("expression_id"))
        and get_node_evaluation_results(
            method, graph, test_id, danger_set, False
        )
    ):
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
