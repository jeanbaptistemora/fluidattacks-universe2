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


def has_console_functions(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_HAS_CONSOLE_FUNCTIONS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                pred_nid = g.pred_ast(graph, nid)[0]
                expr = graph.nodes[pred_nid].get("expression")
                if expr == "Console.WriteLine":
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.has_console_functions",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
