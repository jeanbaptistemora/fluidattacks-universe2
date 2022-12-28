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
    n_attrs = graph.nodes[args.n_id]
    operator = graph.nodes[n_attrs["label_field_operator"]]["label_text"]
    operand = n_attrs["label_field_operand"]
    return build_unary_expression_node(args, operator, operand)
