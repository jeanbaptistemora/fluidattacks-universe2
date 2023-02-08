from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    expr_id = graph.nodes[args.n_id]["label_field_function"]
    expr = node_to_str(graph, expr_id)

    arguments_id = graph.nodes[args.n_id]["label_field_arguments"]

    return build_method_invocation_node(
        args, expr, expr_id, arguments_id, None
    )
