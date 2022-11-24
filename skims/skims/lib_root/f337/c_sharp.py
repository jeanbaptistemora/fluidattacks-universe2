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
    GraphShard,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def get_inner_nodes(graph: Graph, node: NId, label_type: str) -> List[NId]:
    return g.match_ast_group(graph, node, label_type, depth=-1)[label_type]


def controller_class_is_safe(shard: GraphShard, n_id: NId) -> bool:
    return bool(
        shard.syntax_graph
        and (
            class_filter := g.match_ast(
                shard.syntax_graph, n_id, "Attribute", depth=2
            )["Attribute"]
        )
        and (attribute_node := shard.syntax_graph.nodes[class_filter])
        and (attribute_node["name"] == "AutoValidateAntiforgeryToken")
    )


def get_vulns(graph: Graph, n_id: NId) -> Iterable[NId]:
    unsafe_attributes: List[str] = [
        "HttpPost",
        "HttpPut",
        "HttpDelete",
        "HttpPatch",
    ]

    method_declarations: List[NId] = get_inner_nodes(
        graph, n_id, "MethodDeclaration"
    )

    for method_node in method_declarations:
        if attr_node := graph.nodes[method_node].get("attributes_id"):
            attrs = get_inner_nodes(graph, attr_node, "Attribute")
            names = [graph.nodes[attr].get("name") for attr in attrs]
            if (
                any(unsafe_attr in names for unsafe_attr in unsafe_attributes)
                and "ValidateAntiForgeryToken" not in names
            ):
                yield method_node


def has_not_csfr_protection(  # NOSONAR
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_HAS_NOT_CSFR_PROTECTION

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):

            if shard.syntax_graph is None:
                continue
            graph: Graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="Class"),
            ):
                if controller_class_is_safe(shard, n_id):
                    continue

                for vuln in get_vulns(graph, n_id):
                    yield shard, vuln

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f337.cs_has_not_csfr_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
