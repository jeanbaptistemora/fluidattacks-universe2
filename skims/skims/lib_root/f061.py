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


def c_sharp_swallows_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            graph = shard.graph

            for catch_clause in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_clause"),
            ):
                block = g.match_ast(graph, catch_clause, "block")["block"]
                block_childs = g.adj_cfg(graph, block)
                if not block_childs:
                    yield shard, block
                    continue
                first_statement = block_childs[-1]
                if graph.nodes[first_statement]["label_type"] == "comment":
                    yield shard, block

    return get_vulnerabilities_from_n_ids(
        cwe=("390",),
        desc_key="src.lib_path.f061.swallows_exceptions.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def java_swallows_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph

            for catch_clause in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_clause"),
            ):
                block = g.match_ast(graph, catch_clause, "block")["block"]
                block_childs = g.adj_cfg(graph, block)
                if not block_childs:
                    yield shard, block
                    continue

    return get_vulnerabilities_from_n_ids(
        cwe=("390",),
        desc_key="src.lib_path.f061.swallows_exceptions.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F061
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_swallows_exceptions),
    (FINDING, java_swallows_exceptions),
)
