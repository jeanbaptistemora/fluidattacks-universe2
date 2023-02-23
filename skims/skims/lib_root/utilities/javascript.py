from itertools import (
    chain,
)
from model.graph_model import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def _requires_module(graph: Graph, n_id: NId, module_name: str) -> bool:
    n_attrs = graph.nodes[n_id]
    if (
        (method_id := n_attrs.get("value_id"))
        and (method_attrs := graph.nodes[n_attrs["value_id"]])
        and method_attrs["label_type"] == "MethodInvocation"
    ):
        m_name = graph.nodes[method_id].get("expression")
        if (
            m_name == "require"
            and (al_id := graph.nodes[method_id].get("arguments_id"))
            and (arg_id := g.match_ast(graph, al_id).get("__0__"))
            and (import_module := graph.nodes[arg_id].get("value"))
            and import_module[1:-1] == module_name
        ):
            return True
    return False


def file_imports_module(graph: Graph, module_name: str) -> bool:
    for fl_id in g.matching_nodes(graph, label_type="File"):
        import_ids = g.match_ast_group(graph, fl_id, "Import", depth=2)[
            "Import"
        ]
        require_ids = g.match_ast_group_d(graph, fl_id, "VariableDeclaration")
        for n_id in chain(import_ids, require_ids):
            n_attrs = graph.nodes[n_id]
            m_name = n_attrs.get("expression")
            if (
                n_attrs["label_type"] == "Import"
                and m_name
                and m_name[1:-1] == module_name
            ) or _requires_module(graph, n_id, module_name):
                return True
    return False


def get_namespace_alias(graph: Graph, module_name: str) -> str | None:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (node.get("import_type") == "namespace_import")
            and (n_exp := node.get("expression"))
            and (n_exp[1:-1] == module_name)
        )

    nodes = graph.nodes
    if (
        import_n_id := next(
            iter(g.filter_nodes(graph, nodes, predicate_matcher)), None
        )
    ) and (alias := nodes[import_n_id].get("identifier")):
        return alias
    return None


def get_default_alias(graph: Graph, module_name: str) -> str | None:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (n_exp := node.get("expression"))
            and (n_exp[1:-1] == module_name)
        )

    nodes = graph.nodes

    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if (nodes[n_id].get("import_type") == "default_import") and (
            alias := nodes[n_id].get("identifier")
        ):
            return alias
        if (
            (nodes[n_id].get("import_type") == "named_import")
            and (nodes[n_id].get("identifier") == "default")
            and (alias := nodes[n_id].get("label_alias"))
        ):
            return alias

    for var_n_id in g.matching_nodes(graph, label_type="VariableDeclaration"):
        if _requires_module(graph, var_n_id, module_name) and (
            var_name := graph.nodes[var_n_id].get("variable")
        ):
            return var_name
    return None


def get_named_alias(
    graph: Graph, module_name: str, element_name: str
) -> str | None:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (n_exp := node.get("expression"))
            and (n_exp[1:-1] == module_name)
            and (node.get("import_type") == "named_import")
            and (node.get("identifier") == element_name)
        )

    if n_id := next(
        iter(g.filter_nodes(graph, graph.nodes, predicate_matcher)), None
    ):
        if alias := graph.nodes[n_id].get("label_alias"):
            return alias
        return element_name
    return None
