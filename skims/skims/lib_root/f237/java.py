from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def has_print_statements(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> Iterable[graph_model.GraphShardNode]:

        print_methods = {"print", "println"}

        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):

                n_expr = graph.nodes[n_id].get("expression")

                if (
                    n_expr in print_methods
                    and (n_args_id := graph.nodes[n_id].get("arguments_id"))
                    and (
                        args_childs := g.match_ast(
                            graph,
                            n_args_id,
                            "SymbolLookup",
                            "FieldAccess",
                            depth=-1,
                        )
                    )
                    and (
                        args_childs.get("SymbolLookup")
                        or args_childs.get("FieldAccess")
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JAVA_HAS_PRINT_STATEMENTS,
    )
