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
    for method in danger_methods:
        method_set = method.split(".")
        if (
            n_attrs["expression"] == method
            and import_lib + "." + method_set[0] in imps
        ):
            return True
        if len(method_set) == 1:
            expr_id = n_attrs["expression_id"]
            if (
                graph.nodes[expr_id]["label_type"] == "MemberAccess"
                and (member := graph.nodes[expr_id]["member"])
                and member == method
                and (expression := graph.nodes[expr_id]["expression"])
                and expression == import_lib
            ):
                return True
        if len(method_set) == 2:
            if n_attrs["expression"] == import_lib + "." + method:
                return True
    return False
