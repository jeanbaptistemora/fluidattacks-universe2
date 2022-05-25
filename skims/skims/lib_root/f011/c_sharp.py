from lib_root.utilities.c_sharp import (
    get_object_identifiers,
)
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
from utils.string import (
    split_on_last_dot as split_last,
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


def schema_by_url(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_SCHEMA_BY_URL
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):

            if shard.syntax_graph is None:
                continue

            obj_identifiers = get_object_identifiers(
                shard, {"XmlSchemaCollection"}
            )
            s_graph = shard.syntax_graph

            for m_id in g.filter_nodes(
                s_graph,
                s_graph.nodes,
                g.pred_has_labels(label_type="MethodInvocation"),
            ):
                if not (
                    (
                        split_expr := split_last(
                            s_graph.nodes[m_id].get("expression")
                        )
                    )
                    and split_expr[0] in obj_identifiers
                    and split_expr[1] == "Add"
                ):
                    continue
                if (
                    args := g.match_ast_d(s_graph, m_id, "ArgumentList")
                ) and all(
                    (
                        s_graph.nodes[elem].get("label_type") == "Literal"
                        for elem in g.match_ast(s_graph, args).values()
                    )
                ):
                    yield shard, args

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f011.c_sharp_schema_by_url",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
