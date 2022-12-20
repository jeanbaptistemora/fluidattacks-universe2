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


def cs_insecure_channel(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_CHANNEL
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:

        for shard in graph_db.shards_by_language(c_sharp):

            if shard.syntax_graph is None:
                continue

            for obj_nid in g.matching_nodes(
                shard.syntax_graph, label_type="ObjectCreation"
            ):
                if (
                    obj_type := shard.syntax_graph.nodes[obj_nid].get("name")
                ) and obj_type == "FtpClient":
                    yield shard, obj_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f148.cs_insecure_channel",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
