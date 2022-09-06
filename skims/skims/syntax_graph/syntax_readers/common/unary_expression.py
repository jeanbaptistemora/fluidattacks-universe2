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
    node_id = args.ast_graph.nodes[args.n_id]
    operator = args.ast_graph.nodes[node_id["label_field_operator"]][
        "label_text"
    ]
    operand = node_id.get("label_field_operand") or node_id.get(
        "label_field_argument"
    )
    return build_unary_expression_node(args, operator, operand)
