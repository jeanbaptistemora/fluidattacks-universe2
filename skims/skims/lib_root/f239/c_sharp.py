from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
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


def info_leak_errors(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INFO_LEAK_ERRORS
    c_sharp = GraphLanguage.CSHARP

    rules = {"WebHostDefaults.DetailedErrorsKey", '"true"'}

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            for n_id in search_method_invocation_naive(graph, {"UseSetting"}):
                for path in get_backward_paths(graph, n_id):
                    evaluation = evaluate(method, graph, path, n_id)
                    if (
                        evaluation
                        and evaluation.danger
                        and evaluation.triggers == rules
                    ):
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f239.csharp_info_leak_errors",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
