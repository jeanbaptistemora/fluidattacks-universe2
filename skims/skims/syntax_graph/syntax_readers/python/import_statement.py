from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def multiple_import_reader(
    args: SyntaxGraphArgs,
    module_name: str,
    name_id: NId,
    direct_imports: list[NId],
    aliased_imports: list[NId],
) -> NId:
    graph = args.ast_graph
    nodes: list[dict[str, str]] = []
    if name_id in direct_imports:
        direct_imports.remove(name_id)
    for _id in direct_imports:
        nodes.append(
            {
                "module": module_name,
                "imported_value": node_to_str(graph, _id),
                "corrected_n_id": _id,
            }
        )

    if name_id in aliased_imports:
        aliased_imports.remove(name_id)
    for _id in aliased_imports:
        n_attrs = graph.nodes[_id]
        imported_value = node_to_str(graph, n_attrs["label_field_name"])
        imported_alias = node_to_str(graph, n_attrs["label_field_alias"])
        nodes.append(
            {
                "module": module_name,
                "imported_value": imported_value,
                "imported_alias": imported_alias,
                "corrected_n_id": _id,
            }
        )

    return build_import_statement_node(args, *nodes)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    nodes: list[dict[str, str]] = []
    name_id = graph.nodes[args.n_id].get("label_field_module_name")
    if not name_id:
        name_id = graph.nodes[args.n_id]["label_field_name"]

    if graph.nodes[name_id]["label_type"] == "aliased_import":
        n_attrs = graph.nodes[name_id]
        module_name = node_to_str(graph, n_attrs["label_field_name"])
        module_alias = node_to_str(graph, n_attrs["label_field_alias"])
        nodes.append(
            {
                "module": module_name,
                "imported_alias": module_alias,
                "corrected_n_id": name_id,
            }
        )
    else:
        module_name = node_to_str(graph, name_id)
        nodes.append(
            {
                "module": module_name,
                "corrected_n_id": name_id,
            }
        )

    direct_imports = match_ast_group_d(graph, args.n_id, "dotted_name")
    aliased_imports = match_ast_group_d(graph, args.n_id, "aliased_import")

    if (len(direct_imports) + len(aliased_imports)) <= 1:
        return build_import_statement_node(args, *nodes)

    return multiple_import_reader(
        args, module_name, name_id, direct_imports, aliased_imports
    )
