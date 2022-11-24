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
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Iterable,
    Set,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, method_id: NId, class_id: NId) -> bool:
    for path in get_backward_paths(graph, method_id):
        if class_id in path:
            return True
    return False


def get_vuln_nodes(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for c_id in g.filter_nodes(
        graph,
        graph.nodes,
        g.pred_has_labels(label_type="Class"),
    ):
        if not (
            (attr_cid := g.match_ast_d(graph, c_id, "AttributeList"))
            and (childc_id := g.adj_ast(graph, attr_cid)[0])
            and graph.nodes[childc_id].get("name") == "SecurityCritical"
        ):
            continue

        for m_id in g.filter_nodes(
            graph,
            graph.nodes,
            g.pred_has_labels(label_type="MethodDeclaration"),
        ):
            if (
                (attr_mid := g.match_ast_d(graph, m_id, "AttributeList"))
                and (child_id := g.adj_ast(graph, attr_mid)[0])
                and graph.nodes[child_id].get("name") == "SecuritySafeCritical"
                and is_in_path(graph, m_id, c_id)
            ):
                vuln_nodes.add(m_id)
    return vuln_nodes


def conflicting_annotations(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
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
