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
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    value = None
    value_id = match_ast_d(args.ast_graph, args.n_id, "string_content")
    if value_id:
        value = args.ast_graph.nodes[value_id].get("label_text")

    if not value:
        value = node_to_str(args.ast_graph, args.n_id)

    return build_string_literal_node(args, value)
