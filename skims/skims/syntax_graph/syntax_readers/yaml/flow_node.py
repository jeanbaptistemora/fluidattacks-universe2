from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.syntax_nodes.bool_literal import (
    build_bool_literal_node,
)
from syntax_graph.syntax_nodes.number_literal import (
    build_number_literal_node,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def rm_trail_quotes(literal: str) -> str:
    if len(literal) > 2 and (
        literal.startswith('"') or literal.startswith("'")
    ):
        literal = literal[1:-1]
    return literal


def reader(args: SyntaxGraphArgs) -> NId:
    invalid_types = {
        "[",
        "]",
        "{",
        "}",
        ",",
        ";",
    }
    child_id = adj_ast(args.ast_graph, args.n_id)[0]
    if args.ast_graph.nodes[child_id]["label_type"] == "plain_scalar":
        lit_id = adj_ast(args.ast_graph, child_id)[0]
        literal_type = args.ast_graph.nodes[lit_id]["label_type"]
        literal_text = args.ast_graph.nodes[lit_id]["label_text"]
        if literal_type in {"integer_scalar", "float_scalar"}:
            return build_number_literal_node(args, literal_text)
        if literal_type == "boolean_scalar":
            return build_bool_literal_node(args, literal_text)
        if literal_type == "string_scalar":
            return build_string_literal_node(
                args, rm_trail_quotes(literal_text)
            )
    if args.ast_graph.nodes[child_id]["label_type"] == "flow_sequence":
        childs_id = adj_ast(
            args.ast_graph,
            child_id,
        )
        valid_childs = [
            child
            for child in childs_id
            if args.ast_graph.nodes[child]["label_type"] not in invalid_types
        ]
        return build_array_node(args, valid_childs)

    return build_string_literal_node(
        args, node_to_str(args.ast_graph, args.n_id)
    )
