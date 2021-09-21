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


def generic_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.KOTLIN
        ):
            for catch_clause in g.filter_nodes(
                shard.graph,
                shard.graph.nodes,
                g.pred_has_labels(label_type="catch_block"),
            ):
                exception_type_node = g.get_ast_childs(
                    shard.graph, catch_clause, "user_type"
                )
                exception_type = (
                    g.get_ast_childs(
                        shard.graph, exception_type_node[0], "type_identifier"
                    )
                    if exception_type_node
                    else tuple()
                )
                if exception_type and shard.graph.nodes[exception_type[0]][
                    "label_text"
                ] in {"Error", "Exception", "Throwable"}:
                    yield shard, catch_clause

    return get_vulnerabilities_from_n_ids(
        cwe=("397",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
