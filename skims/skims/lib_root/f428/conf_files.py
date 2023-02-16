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


def unapropiated_comment(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_INAPPROPRIATE_ELEMENTS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            if len(g.matching_nodes(graph, label_type="Comment")) >= 1:
                yield shard, "1"

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f428.json_unapropiated_elements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
