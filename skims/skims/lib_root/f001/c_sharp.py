from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
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


def sql_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    danger_methods = {"ExecuteSqlCommand"}
    danger_objects = {"SqlCommand"}
    method = core_model.MethodsEnum.CS_SQL_INJECTION

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in [
                *search_method_invocation_naive(graph, danger_methods),
                *yield_syntax_graph_object_creation(graph, danger_objects),
            ]:
                test_nid = g.adj_ast(
                    graph,
                    graph.nodes[nid].get("arguments_id"),
                )[0]
                for path in get_backward_paths(graph, test_nid):
                    evaluation = evaluate(method, graph, path, test_nid)
                    if evaluation and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.001.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
