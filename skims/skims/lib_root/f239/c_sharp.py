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


def is_node_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_INFO_LEAK_ERRORS
    rules = {"WebHostDefaults.DetailedErrorsKey", '"true"'}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def info_leak_errors(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INFO_LEAK_ERRORS
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"UseSetting"}):
                if is_node_danger(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f239.csharp_info_leak_errors",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
