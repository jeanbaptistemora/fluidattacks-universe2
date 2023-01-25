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
from symbolic_eval.utils import (
    get_object_identifiers,
)
from typing import (
    Iterable,
    List,
    Optional,
)
from utils import (
    graph as g,
)
from utils.string import (
    split_on_last_dot as split_last,
)


def is_insec_squema(
    graph: Graph, n_id: str, identifiers: List[str]
) -> Optional[NId]:
    if not (
        (split_expr := split_last(graph.nodes[n_id].get("expression")))
        and split_expr[0] in identifiers
        and split_expr[1] == "Add"
    ):
        return None

    if (args := g.match_ast_d(graph, n_id, "ArgumentList")) and all(
        (
            graph.nodes[elem].get("label_type") == "Literal"
            for elem in g.match_ast(graph, args).values()
        )
    ):
        return args

    return None


def xsl_transform_object(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_XSL_TRANSFORM_OBJECT
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for obj_nid in g.matching_nodes(
                graph,
                label_type="ObjectCreation",
            ):
                if (
                    obj_type := graph.nodes[obj_nid].get("name")
                ) and obj_type == "XslTransform":
                    yield shard, obj_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f011.csharp_xsl_transform_object",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def schema_by_url(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_SCHEMA_BY_URL
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            obj_identifiers = get_object_identifiers(
                graph, {"XmlSchemaCollection"}
            )

            for m_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                if args := is_insec_squema(graph, m_id, obj_identifiers):
                    yield shard, args

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f011.c_sharp_schema_by_url",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
