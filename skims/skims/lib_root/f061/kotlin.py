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


def swallows_exceptions(
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
                catch_block = g.get_ast_childs(
                    shard.graph, catch_clause, "statements"
                )
                only_comments = (
                    all(
                        shard.graph.nodes[node]["label_type"] == "comment"
                        for node in g.adj_ast(shard.graph, catch_block[0])
                    )
                    if catch_block
                    else False
                )
                if not catch_block or only_comments:
                    yield shard, catch_clause

    return get_vulnerabilities_from_n_ids(
        cwe=("390",),
        desc_key="src.lib_path.f061.swallows_exceptions.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F061
