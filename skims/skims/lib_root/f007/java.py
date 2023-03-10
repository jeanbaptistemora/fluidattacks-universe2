from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def csrf_protections_disabled(graph_db: GraphDB) -> Vulnerabilities:
    csrf_methods = {"disable", "ignoringAntMatchers"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                expr_id = graph.nodes[n_id]["expression_id"]
                if (
                    graph.nodes[expr_id].get("symbol") == "csrf"
                    and (parent_id := g.pred_ast(graph, n_id)[0])
                    and (
                        expr_id := graph.nodes[parent_id].get("expression_id")
                    )
                    and graph.nodes[expr_id].get("symbol") in csrf_methods
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f007.csrf_protections_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_CSRF_PROTECTIONS_DISABLED,
    )
