from itertools import (
    chain,
)
from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Optional,
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


def get_namespace_alias(graph: Graph, module_name: str) -> Optional[str]:
    if (
        namespace_import_n_ids := g.matching_nodes(
            graph,
            label_type="Import",
            import_type="namespace_import",
            expression='"' + module_name + '"',
        )
    ) and (alias := graph.nodes[namespace_import_n_ids[0]].get("identifier")):
        return alias
    return None
