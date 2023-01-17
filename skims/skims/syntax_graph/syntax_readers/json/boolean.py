from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.bool_literal import (
    build_bool_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    value = n_attrs["label_text"]
    return build_bool_literal_node(args, value)
