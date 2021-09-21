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
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT
        ):
            graph = shard.graph
            for catch_clause in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_clause"),
            ):
                statement_block = g.match_ast(
                    graph, catch_clause, "statement_block"
                )["statement_block"]
                block_childs = g.adj_ast(graph, statement_block)[1:-1]
                only_comments = all(
                    graph.nodes[node]["label_type"] == "comment"
                    for node in block_childs
                )
                if not block_childs or only_comments:
                    yield shard, catch_clause

            for call_expression in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="call_expression"),
            ):
                match = g.match_ast(
                    graph,
                    call_expression,
                    "member_expression",
                    "arguments",
                )
                if member_expression := match["member_expression"]:
                    match_name = g.match_ast(
                        graph, member_expression, "property_identifier"
                    )
                    if name := match_name["property_identifier"]:
                        name = graph.nodes[name]["label_text"]
                        if (
                            name == "catch"
                            # .catch()
                            and len(g.adj_ast(graph, match["arguments"])) < 3
                        ):
                            yield shard, call_expression

    return get_vulnerabilities_from_n_ids(
        cwe=("390",),
        desc_key="src.lib_path.f061.swallows_exceptions.description",
        desc_params=dict(lang="Javascript"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F061
