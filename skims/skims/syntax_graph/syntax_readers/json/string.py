from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    value = ""
    value_id = match_ast_d(args.ast_graph, args.n_id, "string_content")
    if value_id:
        value = args.ast_graph.nodes[value_id]["label_text"]

    return build_string_literal_node(args, value)
