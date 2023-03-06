from model.graph_model import (
    Graph,
)
import utils.graph as g


def get_all_imports_exp(graph: Graph) -> list[str]:
    imports = []
    for n_id in g.matching_nodes(
        graph,
        label_type="Import",
    ):
        imports.append(graph.nodes[n_id]["expression"])
    return imports


def check_method_origin(
    graph: Graph, import_lib: str, danger_methods: set, n_attrs: dict
) -> bool:
    imps = get_all_imports_exp(graph)
    expr_id = n_attrs["expression_id"]
    if (
        graph.nodes[expr_id]["label_type"] == "MemberAccess"
        and (member := graph.nodes[expr_id]["member"])
        and member in danger_methods
        and (expression := graph.nodes[expr_id]["expression"])
        and expression == import_lib
    ):
        return True
    if (
        graph.nodes[expr_id]["label_type"] == "SymbolLookup"
        and (symbol := graph.nodes[expr_id]["symbol"])
        and symbol in danger_methods
        and import_lib + "." + symbol in imps
    ):
        return True
    return False
