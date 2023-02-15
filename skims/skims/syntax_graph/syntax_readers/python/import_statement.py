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


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    nodes: list[dict[str, str]] = []
    name_id = graph.nodes[args.n_id].get("label_field_module_name")
    if not name_id:
        name_id = graph.nodes[args.n_id]["label_field_name"]

    module_name = node_to_str(graph, name_id)
    nodes.append(
        {
            "expression": module_name,
            "corrected_n_id": name_id,
        }
    )

    imported_names = match_ast_group_d(graph, args.n_id, "dotted_name")
    for _id in imported_names[1:]:
        nodes.append(
            {
                "expression": module_name,
                "identifier": node_to_str(graph, _id),
                "corrected_n_id": _id,
            }
        )

    return build_import_statement_node(args, *nodes)
