from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    field_node = args.ast_graph.nodes[args.n_id]["label_field_name"]
    return build_named_argument_node(args, None, field_node)
