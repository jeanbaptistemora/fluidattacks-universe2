from collections.abc import (
    Iterator,
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
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, method_id: NId, class_id: NId) -> bool:
    for path in get_backward_paths(graph, method_id):
        if class_id in path:
            return True
    return False


def get_action_filter(graph: Graph, n_id: NId, filter_name: str) -> NId | None:
    if attr_list_ids := g.match_ast_group_d(graph, n_id, "AttributeList"):
        for attr_id in attr_list_ids:
            if f_node := g.adj_ast(graph, attr_id)[0]:
                if (
                    f_name := graph.nodes[f_node].get("name")
                ) and f_name == filter_name:
                    return f_node
    return None


def get_vuln_nodes(graph: Graph) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for c_id in g.matching_nodes(graph, label_type="Class"):

        if not get_action_filter(graph, c_id, "SecurityCritical"):
            continue

        for m_id in g.matching_nodes(graph, label_type="MethodDeclaration"):

            if (
                filter_node := get_action_filter(
                    graph, m_id, "SecuritySafeCritical"
                )
            ) and is_in_path(graph, m_id, c_id):
                vuln_nodes.add(filter_node)

    return vuln_nodes


def conflicting_annotations(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for m_id in get_vuln_nodes(graph):
                yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f366.conflicting_transparency_annotations",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_CONFLICTING_ANNOTATIONS,
    )
