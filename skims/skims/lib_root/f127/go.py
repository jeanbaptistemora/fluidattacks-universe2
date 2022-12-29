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
import utils.graph as g


def get_eval_result(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"isinfcheck", "isnancheck"}
        ):
            return True
    return False


def go_insecure_query_float(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.GO_INSECURE_QUERY_FLOAT
    danger_methods = {
        "DBQuerySameFile",
        "Exec",
        "ExecContext",
        "Query",
        "QueryContext",
        "QueryRow",
        "QueryRowContext",
    }

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                m_name = graph.nodes[n_id]["expression"].split(".")
                if (
                    m_name[-1] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and get_eval_result(graph, al_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="F127.title",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
