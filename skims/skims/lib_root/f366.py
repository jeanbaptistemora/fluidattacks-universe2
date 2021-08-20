from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def csharp_conflicting_annotations(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="class_declaration"),
            ):
                class_annotation = g.get_ast_childs(
                    shard.graph, member, label_type="attribute_list"
                )
                if len(class_annotation) > 0:
                    val_class_ann = g.get_ast_childs(
                        shard.graph,
                        class_annotation[0],
                        label_type="identifier",
                        depth=2,
                    )
                    if (
                        shard.graph.nodes[val_class_ann[0]].get("label_text")
                        == "SecurityCritical"
                    ):
                        critical = True
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="method_declaration"),
            ):
                method_annotation = g.get_ast_childs(
                    shard.graph, member, label_type="attribute_list"
                )
                if len(method_annotation) > 0:
                    val_method_ann = g.get_ast_childs(
                        shard.graph,
                        method_annotation[0],
                        label_type="identifier",
                        depth=2,
                    )
                    if (
                        shard.graph.nodes[val_method_ann[0]].get("label_text")
                        == "SecuritySafeCritical"
                        and critical
                    ):
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("749",),
        desc_key="F366.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F366
QUERIES: graph_model.Queries = ((FINDING, csharp_conflicting_annotations),)
