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


def uses_eval(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_USES_EVAL

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="expression_statement"),
            ):
                if node_to_str(shard.graph, member).startswith("eval"):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f143.js_uses_eval",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
