from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_statement import (
    build_switch_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
    value_id = args.ast_graph.nodes[args.n_id]["label_field_value"]

    return build_switch_statement_node(args, body_id, value_id)
