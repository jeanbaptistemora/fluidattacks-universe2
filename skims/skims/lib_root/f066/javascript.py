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
from utils.graph.text_nodes import (
    node_to_str,
)


def uses_console_log(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_USES_CONSOLE_LOG

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            graph = shard.graph
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="call_expression"),
            ):
                match = g.match_ast(
                    graph,
                    member,
                    "member_expression",
                    "identifier",
                )

                if member_expression_id := match["member_expression"]:
                    method_name = node_to_str(graph, member_expression_id)
                    if method_name == "console.log":
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.js_uses_console_log",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
