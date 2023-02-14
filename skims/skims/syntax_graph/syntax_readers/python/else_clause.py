from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.else_clause import (
    build_else_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]

    return build_else_clause_node(args, body_id)
