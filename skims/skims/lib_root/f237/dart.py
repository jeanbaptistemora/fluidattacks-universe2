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


def get_print_methods(graph: Graph) -> set[str]:
    print_methods: set[str] = {"print"}
    nodes = graph.nodes
    for n_id in g.matching_nodes(graph, label_type="Import"):
        imported_package = nodes[n_id].get("expression")
        if imported_package == "'package:flutter/foundation.dart'":
            if alias := nodes[n_id].get("label_alias"):
                print_method = f"{alias}.debugPrint"
            else:
                print_method = "debugPrint"
            print_methods.add(print_method)
        if imported_package == "'dart:developer'":
            if alias := nodes[n_id].get("label_alias"):
                print_method = f"{alias}.log"
            else:
                print_method = "log"
            print_methods.add(print_method)

    return print_methods


def get_expression(graph: Graph, n_id: NId) -> str:
    parent = g.pred_ast(graph, n_id)[0]
    expr = graph.nodes[n_id].get("symbol")
    if (selector_n_id := g.match_ast_d(graph, parent, "Selector")) and (
        selector := graph.nodes[selector_n_id].get("selector_name")
    ):
        expr = f"{expr}.{selector}"
    return expr


def prints_danger_values(graph: Graph, n_id: NId) -> bool:
    parent = g.pred_ast(graph, n_id)[0]
    if (args_n_id := g.match_ast_d(graph, parent, "ArgumentList")) and (
        g.match_ast_d(graph, args_n_id, "SymbolLookup")
    ):
        return True
    return False


def n_expression(graph: Graph, n_id: NId) -> str:
    n_expr = graph.nodes[n_id]["symbol"]
    parent = g.pred_ast(graph, n_id)[0]
    if graph.nodes[parent]["label_type"] == "MethodInvocation":
        n_expr = graph.nodes[parent]["expression"]
    return n_expr


def has_print_statements(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.DART,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            print_methods = get_print_methods(graph)
            for n_id in g.matching_nodes(
                graph,
                label_type="SymbolLookup",
            ):
                n_expr = n_expression(graph, n_id)
                if n_expr in print_methods and prints_danger_values(
                    graph, n_id
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.DART_HAS_PRINT_STATEMENTS,
    )
