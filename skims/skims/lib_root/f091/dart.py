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
    GraphShardMetadataLanguage,
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
from typing import (
    Any,
    List,
)
from utils import (
    graph as g,
)


def is_logger_unsafe(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.DART_INSECURE_LOGGING
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True

    return False


def get_expression(graph: Graph, n_id: NId) -> List[Any]:
    parent = g.pred_ast(graph, n_id)[0]
    expr = graph.nodes[n_id].get("symbol")
    selector_n_id = g.match_ast_d(graph, parent, "Selector")
    selector = graph.nodes.get(selector_n_id, {}).get("selector_name")
    return [expr, selector] if selector else [expr]


def dart_insecure_logging(graph_db: GraphDB) -> Vulnerabilities:
    log_members = {"log", "logger"}
    log_methods = {
        "fine",
        "finest",
        "config",
        "info",
        "warning",
        "severe",
        "shout",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.DART
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="SymbolLookup"):
                if (n_expr := get_expression(shard.syntax_graph, nid)) and (
                    n_expr[0] in log_members
                    and (len(n_expr) == 1 or n_expr[1] in log_methods)
                    and is_logger_unsafe(graph, nid)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.DART_INSECURE_LOGGING,
    )
