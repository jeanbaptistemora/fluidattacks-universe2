from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
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
    expr_id = adj_ast(graph, args.n_id)[0]
    expr = node_to_str(graph, expr_id)

    suffix_id = match_ast_d(
        args.ast_graph, args.n_id, "value_argument", depth=3
    )
    args_id = None
    if suffix_id:
        args_id = graph.nodes[suffix_id].get("label_field_value")
    return build_method_invocation_node(args, expr, expr_id, args_id, None)
