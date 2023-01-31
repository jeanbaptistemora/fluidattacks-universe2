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
from typing import (
    Iterable,
    Set,
)
from utils import (
    graph as g,
)


def get_print_methods(graph: Graph) -> Set[str]:
    print_methods: Set[str] = {"print"}
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


def prints_danger_values(graph: Graph, n_id: NId) -> bool:
    parent = g.pred_ast(graph, n_id)[0]
    class_childs = list(g.adj_ast(graph, parent))
    if (
        len(class_childs) > class_childs.index(n_id)
        and (al_id := class_childs[class_childs.index(n_id) + 1])
        and graph.nodes[al_id]["label_type"] == "ArgumentList"
        and (
            args_childs := g.match_ast(graph, al_id, "SymbolLookup", depth=-1)
        )
        and args_childs.get("SymbolLookup")
    ):
        return True
    return False


def has_print_statements(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.DART,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            print_methods = get_print_methods(graph)

            for n_id in g.matching_nodes(graph, label_type="SymbolLookup"):
                n_expr = graph.nodes[n_id].get("symbol")
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
