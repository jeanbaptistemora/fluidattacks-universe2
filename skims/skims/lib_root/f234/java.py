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
from utils import (
    graph as g,
)


def get_vuln_nodes(graph: Graph) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for n_id in g.matching_nodes(graph, label_type="CatchClause"):
        childs = g.match_ast(graph, n_id, "CatchParameter", "ExecutionBlock")
        param = childs.get("CatchParameter")
        block = childs.get("ExecutionBlock")

        if not (param and block):
            continue
        exc_name = graph.nodes[param].get("variable_name")

        for m_id in g.filter_nodes(
            graph,
            nodes=g.adj_ast(graph, str(block), depth=-1),
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            m_node = graph.nodes[m_id]
            if (
                m_node["expression"] == "printStackTrace"
                and (symbol_id := m_node.get("object_id"))
                and graph.nodes[symbol_id]["symbol"] == exc_name
            ):
                vuln_nodes.add(m_id)

    return vuln_nodes


def info_leak_stacktrace(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id in get_vuln_nodes(graph):
                yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f234.java_info_leak_stacktrace",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_LEAK_STACKTRACE,
    )
