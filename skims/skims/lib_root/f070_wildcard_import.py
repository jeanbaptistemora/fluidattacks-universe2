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


def java_wildcard_import(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            for import_dcl_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="import_declaration"),
            ):
                import_dcl_c_ids = g.adj_ast(shard.graph, import_dcl_id)
                static_id = import_dcl_c_ids[1]
                static_attrs = shard.graph.nodes[static_id]
                last_id = import_dcl_c_ids[-2]
                last_attrs = shard.graph.nodes[last_id]

                if (
                    last_attrs["label_type"] == "asterisk"
                    and static_attrs["label_type"] != "static"
                ):
                    yield shard, import_dcl_id

    return get_vulnerabilities_from_n_ids(
        cwe=("398",),
        desc_key="src.lib_path.f070_wildcard_import.wildcard_import",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def go_wildcard_import(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.GO,
        ):
            for import_dcl_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="import_spec"),
            ):
                import_dcl_c_ids = g.adj_ast(shard.graph, import_dcl_id)
                import_identifier_id = import_dcl_c_ids[0]
                import_identifier = shard.graph.nodes[import_identifier_id]
                if import_identifier["label_type"] == "dot":
                    yield shard, import_dcl_id

    return get_vulnerabilities_from_n_ids(
        cwe=("398",),
        desc_key="src.lib_path.f070_wildcard_import.wildcard_import",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def kotlin_wildcard_import(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.KOTLIN
        ):
            for import_dcl_id in g.filter_nodes(
                shard.graph,
                shard.graph.nodes,
                g.pred_has_labels(label_type="import_header"),
            ):
                wildcard = g.get_ast_childs(
                    shard.graph, import_dcl_id, "point_star"
                )
                if wildcard:
                    yield shard, import_dcl_id

    return get_vulnerabilities_from_n_ids(
        cwe=("398",),
        desc_key="src.lib_path.f070_wildcard_import.wildcard_import",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F070
QUERIES: graph_model.Queries = (
    (FINDING, java_wildcard_import),
    (FINDING, go_wildcard_import),
    (FINDING, kotlin_wildcard_import),
)
