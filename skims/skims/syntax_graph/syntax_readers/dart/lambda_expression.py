from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    f_body = match_ast_d(graph, args.n_id, "function_body")
    block_id = None
    if f_body:
        block_id = match_ast_d(graph, f_body, "block")

    f_signature = match_ast_d(graph, args.n_id, "function_signature")
    name = None
    parameters_id = None
    if f_signature:
        n_attrs = graph.nodes[f_signature]
        name = node_to_str(graph, n_attrs["label_field_name"])
        parameters_id = match_ast_d(
            graph, f_signature, "formal_parameter_list"
        )

    if parameters_id and "__0__" not in match_ast(
        graph, parameters_id, "(", ")"
    ):
        parameters_id = None

    children_nid = {"parameters_id": parameters_id}

    return build_method_declaration_node(args, name, block_id, children_nid)
