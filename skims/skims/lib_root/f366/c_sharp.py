from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, method_id: NId, class_id: NId) -> bool:
    for path in get_backward_paths(graph, method_id):
        if class_id in path:
            return True
    return False


def conflicting_annotations(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for class_id in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="Class"),
            ):
                if not (
                    (
                        attr_cid := g.match_ast(
                            graph, class_id, "AttributeList"
                        ).get("AttributeList")
                    )
                    and graph.nodes[g.adj_ast(graph, attr_cid)[0]].get("name")
                    == "SecurityCritical"
                ):
                    continue
                for method_id in g.filter_nodes(
                    graph,
                    graph.nodes,
                    g.pred_has_labels(label_type="MethodDeclaration"),
                ):
                    if (
                        (
                            attr_mid := g.match_ast(
                                graph, method_id, "AttributeList"
                            ).get("AttributeList")
                        )
                        and graph.nodes[g.adj_ast(graph, attr_mid)[0]].get(
                            "name"
                        )
                        == "SecuritySafeCritical"
                        and is_in_path(graph, method_id, class_id)
                    ):
                        yield shard, method_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f366.conflicting_transparency_annotations",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_CONFLICTING_ANNOTATIONS,
    )
