from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def weak_protocol(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_WEAK_PROTOCOL

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                c_ident = g.get_ast_childs(shard.graph, member, "identifier")
                if (
                    len(c_ident) == 2
                    and shard.graph.nodes[c_ident[0]]["label_text"]
                    == "SecurityProtocolType"
                    and shard.graph.nodes[c_ident[1]]["label_text"]
                    in {"Ssl3", "Tls", "None"}
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
