from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
    search_pred_until_type,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    body_parents = {
        "class_body",
        "extension_body",
        "lambda_expression",
        "program",
    }

    name_id = graph.nodes[args.n_id]["label_field_name"]
    m_name = node_to_str(graph, name_id)

    class_pred, last_c = search_pred_until_type(
        graph,
        args.n_id,
        body_parents,
    )
    if last_c and (class_childs := list(adj_ast(graph, class_pred))):
        pm_id = match_ast_group_d(graph, args.n_id, "formal_parameter_list")
        children = {"parameters_id": pm_id}
        body_id = class_childs[class_childs.index(last_c) + 1]
        return build_method_declaration_node(args, m_name, body_id, children)

    raise MissingCaseHandling(f"Bad functionsignature handling in {args.n_id}")
