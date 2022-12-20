from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
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


def check_default_usehsts(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CHECK_DEFAULT_USEHSTS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            syntax_graph = shard.syntax_graph
            for nid in g.matching_nodes(
                syntax_graph, label_type="MethodInvocation"
            ):
                node_member = syntax_graph.nodes[nid]
                expr_id = syntax_graph.nodes[node_member["expression_id"]]
                if (
                    expr_id := syntax_graph.nodes[node_member["expression_id"]]
                    and expr_id["label_type"] == "MemberAccess"
                    and expr_id["member"] == "UseHsts"
                    and node_member.get("arguments_id") is None
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.check_default_usehsts",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
