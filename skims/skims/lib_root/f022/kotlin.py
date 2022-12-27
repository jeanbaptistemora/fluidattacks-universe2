from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
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


def is_unsafe_param(graph: Graph, n_id: NId) -> bool:
    al_id = graph.nodes[n_id].get("arguments_id")
    if (
        al_id
        and (childs := g.adj_ast(graph, al_id))
        and len(childs) > 0
        and (member := graph.nodes[childs[0]].get("member"))
    ):
        return member == "CLEARTEXT"
    return False


def unencrypted_channel(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"FTPClient", "SMTPClient", "TelnetClient"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if n_attrs["expression"] in danger_methods or (
                    n_attrs["expression"] == "ConnectionSpec.Builder"
                    and is_unsafe_param(graph, n_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f022.unencrypted_channel",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.KT_UNENCRYPTED_CHANNEL,
    )
