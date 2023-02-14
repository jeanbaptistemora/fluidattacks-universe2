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
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    text = node_to_str(graph, args.n_id)
    if interp := match_ast_d(graph, args.n_id, "interpolation"):
        invocations = match_ast_group_d(graph, interp, "attribute")
        return build_string_literal_node(args, text, None, invocations)

    return build_string_literal_node(args, text)
