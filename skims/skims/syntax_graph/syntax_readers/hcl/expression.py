from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
)
from syntax_graph.syntax_nodes.object import (
    build_object_node,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    invalid_types = {
        "tuple_start",
        "tuple_end",
        "{",
        "}",
        ",",
        ";",
    }
    child_id = adj_ast(graph, args.n_id)[0]
    if graph.nodes[child_id]["label_type"] == "collection_value":
        body_id = adj_ast(graph, child_id)[0]
        if graph.nodes[body_id]["label_type"] == "tuple":
            valid_childs = [
                child
                for child in adj_ast(graph, body_id)
                if graph.nodes[child]["label_type"] not in invalid_types
            ]
            return build_array_node(args, valid_childs)
        return build_object_node(
            args,
            c_ids=(
                _id
                for _id in adj_ast(graph, str(body_id))
                if graph.nodes[_id]["label_type"] in {"object_elem"}
            ),
        )
    if graph.nodes[child_id]["label_type"] == "function_call":
        expr_id = match_ast_d(args.ast_graph, child_id, "identifier")
        expr = node_to_str(graph, str(expr_id))
        function_args = match_ast_d(
            args.ast_graph, child_id, "function_arguments"
        )
        args_id = adj_ast(graph, str(function_args))[0]

        return build_method_invocation_node(
            args, expr, str(expr_id), args_id, None
        )
    if graph.nodes[child_id]["label_type"] == "template_expr":
        template = match_ast_d(args.ast_graph, child_id, "quoted_template")
        if not template:
            template_text = node_to_str(graph, child_id)
            start_json = template_text.index("{")
            end_json = template_text[::-1].index("}")
            return build_string_literal_node(
                args, template_text[start_json:-end_json]
            )

    literal_text = node_to_str(graph, args.n_id)
    if literal_text[0] == '"':
        literal_text = literal_text[1:-1]
    return build_string_literal_node(args, literal_text)
