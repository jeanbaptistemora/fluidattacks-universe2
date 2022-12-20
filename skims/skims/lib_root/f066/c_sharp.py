from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
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


def has_console_functions(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_HAS_CONSOLE_FUNCTIONS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
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
