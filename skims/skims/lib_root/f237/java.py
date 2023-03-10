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


def has_print_statements(
    graph_db: GraphDB,
) -> Vulnerabilities:
    print_methods = {"print", "println"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                if (
                    graph.nodes[n_id].get("expression") in print_methods
                    and (args_id := graph.nodes[n_id].get("arguments_id"))
                    and g.match_ast_d(
                        graph,
                        args_id,
                        "SymbolLookup",
                        depth=-1,
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_HAS_PRINT_STATEMENTS,
    )
