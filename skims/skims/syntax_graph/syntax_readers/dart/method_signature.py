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
    match_ast,
    search_pred_until_type,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = adj_ast(graph, args.n_id)
    if (
        len(childs) == 1
        and graph.nodes[childs[0]]["label_type"] == "function_signature"
    ):
        return args.generic(args.fork_n_id(childs[0]))

    body_parents = {
        "class_body",
        "extension_body",
    }
    m_name = None

    class_pred, last_c = search_pred_until_type(
        graph,
        args.n_id,
        body_parents,
    )
    if last_c and (class_childs := list(adj_ast(graph, class_pred))):
        al_list = match_ast(
            graph, args.n_id, "formal_parameter_list", "static"
        )

        parameters_id = al_list.get("formal_parameter_list")
        if not parameters_id:
            parameters_list = []
        else:
            parameters_list = [parameters_id]

        initializers_id = al_list.get("formal_parameter_list")
        if not initializers_id:
            initializers_list = []
        else:
            initializers_list = [initializers_id]
        children = {
            "parameters_id": parameters_list,
            "initializers": initializers_list,
        }
        body_id = class_childs[class_childs.index(last_c) + 1]
        return build_method_declaration_node(args, m_name, body_id, children)

    raise MissingCaseHandling(f"Bad functionsignature handling in {args.n_id}")
