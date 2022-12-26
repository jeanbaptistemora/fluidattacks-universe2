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
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    call_node = args.ast_graph.nodes[args.n_id]
    method_id = call_node["label_field_function"]
    expr = node_to_str(args.ast_graph, method_id)

    args_id = call_node["label_field_arguments"]
    if "__0__" not in match_ast(args.ast_graph, args_id, "(", ")"):
        args_id = None

    return build_method_invocation_node(args, expr, method_id, args_id, None)
