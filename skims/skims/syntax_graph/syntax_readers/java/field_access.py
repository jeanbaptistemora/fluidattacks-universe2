from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.field_access import (
    build_field_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    field_text = args.ast_graph.nodes[args.n_id]["label_text"]
    return build_field_access_node(args, field_text)
