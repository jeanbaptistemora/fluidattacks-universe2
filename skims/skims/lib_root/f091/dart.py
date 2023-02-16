from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
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
    List,
)
from utils import (
    graph as g,
)


def is_logger_unsafe(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.JAVA_INSECURE_LOGGING
    if test_node := graph.nodes[n_id].get("arguments_id"):
        for path in get_backward_paths(graph, test_node):
            evaluation = evaluate(method, graph, path, test_node)
            if (
                evaluation
                and evaluation.danger
                and "userparams" in evaluation.triggers
                and not (
                    "sanitized" in evaluation.triggers
                    and "characters" in evaluation.triggers
                )
            ):
                return True

    return False


def get_expression(graph: Graph, n_id: NId) -> List[str]:
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
    nodes = [
        (shard, n_id)
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.DART
        )
        if shard.syntax_graph
        for n_id in g.matching_nodes(
            shard.syntax_graph, label_type="SymbolLookup"
        )
        if (n_expr := get_expression(shard.syntax_graph, n_id))
        and (
            n_expr[0] in log_members
            and (len(n_expr) == 1 or n_expr[1] in log_methods)
            and is_logger_unsafe(shard.syntax_graph, n_id)
        )
    ]
    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=nodes,
        method=MethodsEnum.DART_INSECURE_LOGGING,
    )
