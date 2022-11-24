from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.null_literal import (
    build_null_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    return build_null_literal_node(args, value=n_attrs["label_text"])
