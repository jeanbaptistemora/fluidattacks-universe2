# Third party libraries
from lib_root.common import (
    GraphShardNodes,
    get_vulnerabilities_from_n_ids
)

# Local libraries
from utils import (
    graph as g,
)
from utils.model import (
    FindingEnum,
    GraphDB,
    LibRootQueries,
    Vulnerabilities,
)


def java_declaration_of_throws_for_generic_exception(
    graph_db: GraphDB,
) -> Vulnerabilities:

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards:
            graph = shard.graph

            for method_declaration_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type='method_declaration'),
            ):
                for throws_id in g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, method_declaration_id),
                    predicate=g.pred_has_labels(label_type='throws'),
                ):
                    c_ids = g.adj_ast(graph, throws_id)

                    for identifier_id in g.filter_nodes(
                        graph,
                        nodes=c_ids,
                        predicate=g.pred_has_labels(
                            label_type='type_identifier',
                        ),
                    ) + g.filter_nodes(
                        graph,
                        nodes=c_ids,
                        predicate=g.pred_has_labels(
                            label_type='scoped_type_identifier',
                        ),
                    ):
                        if graph.nodes[identifier_id]['label_text'] in {
                            'Exception',
                            'Throwable',
                            'lang.Exception',
                            'lang.Throwable',
                            'java.lang.Exception',
                            'java.lang.Throwable',
                        }:
                            yield shard, identifier_id

    return get_vulnerabilities_from_n_ids(
        cwe=(
            '397',
        ),
        desc_key='src.lib_path.f060.insecure_exceptions.description',
        desc_params=dict(lang='Java'),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: FindingEnum = FindingEnum.F060
QUERIES: LibRootQueries = (
    java_declaration_of_throws_for_generic_exception,
)
