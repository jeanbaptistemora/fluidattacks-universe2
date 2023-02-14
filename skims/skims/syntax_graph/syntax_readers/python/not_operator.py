from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.unary_expression import (
    build_unary_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    operand = graph.nodes[args.n_id]["label_field_argument"]
    return build_unary_expression_node(args, "not", operand)
