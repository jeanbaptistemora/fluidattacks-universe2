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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def csrf_protections_disabled(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> Iterable[graph_model.GraphShardNode]:

        csrf_methods = {
            "disable",
            "ignoringAntMatchers",
        }

        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                expr_id = graph.nodes[n_id]["expression_id"]
                if (
                    graph.nodes[expr_id].get("symbol") == "csrf"
                    and (me_pred := g.pred_ast(graph, n_id)[0])
                    and (
                        upper_expr := graph.nodes[me_pred].get("expression_id")
                    )
                    and graph.nodes[upper_expr].get("symbol") in csrf_methods
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f007.csrf_protections_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JAVA_CSRF_PROTECTIONS_DISABLED,
    )
