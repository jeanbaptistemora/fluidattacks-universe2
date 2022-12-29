from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_statement import (
    build_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
    return build_for_statement_node(args, None, None, None, body_id)
