from collections.abc import (
    Iterator,
)
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


def has_print_statements(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> Iterator[graph_model.GraphShardNode]:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_expr = graph.nodes[n_id].get("expression")
                if (
                    n_expr == "print"
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and g.match_ast_d(graph, al_id, "SymbolLookup", depth=-1)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.PYTHON_HAS_PRINT_STATEMENTS,
    )
