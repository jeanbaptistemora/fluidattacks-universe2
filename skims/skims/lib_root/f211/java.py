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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_node_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_VULN_REGEX
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"SafeRegex"}
            and evaluation.triggers == {"UserParams", "HttpParams"}
        ):
            return True
    return False


def analyze_method_vuln(graph: Graph, method_id: NId) -> bool:

    args_id = g.get_ast_childs(graph, method_id, "ArgumentList")
    if args_id:
        args_nids = g.adj_ast(graph, args_id[0])
        if args_nids and len(args_nids) >= 1:
            return is_node_danger(graph, method_id)
    return False


def java_vuln_regular_expression(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_VULN_REGEX
    regex_methods = {"matches"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="MethodInvocation"):
                if graph.nodes[nid].get(
                    "expression"
                ) in regex_methods and analyze_method_vuln(graph, nid):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
