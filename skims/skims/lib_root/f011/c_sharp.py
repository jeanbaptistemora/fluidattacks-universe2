from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def xsl_transform_object(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_XSL_TRANSFORM_OBJECT
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):

            if shard.syntax_graph is None:
                continue

            for obj_nid in g.filter_nodes(
                shard.syntax_graph,
                nodes=shard.syntax_graph.nodes,
                predicate=g.pred_has_labels(label_type="ObjectCreation"),
            ):
                if (
                    obj_type := shard.syntax_graph.nodes[obj_nid].get("name")
                ) and obj_type == "XslTransform":
                    yield shard, obj_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f011.csharp_xsl_transform_object",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
