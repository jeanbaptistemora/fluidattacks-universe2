from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def uses_exit_method(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JAVA_LEAK_STACKTRACE

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="expression_statement"),
            ):
                match = g.match_ast(
                    graph,
                    member,
                    "method_invocation",
                )
                if match["method_invocation"]:
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.js_uses_console_log",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
