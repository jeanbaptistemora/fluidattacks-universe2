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

    suffix_id = match_ast_d(args.ast_graph, args.n_id, "call_suffix")
    args_id = None
    if suffix_id:
        args_id = graph.nodes[suffix_id]["label_field_value_arguments"]

    return build_method_invocation_node(args, expr, expr_id, args_id, None)
