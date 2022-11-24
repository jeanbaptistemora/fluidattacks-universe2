from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.number_literal import (
    build_number_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    return build_number_literal_node(args, value=n_attrs["label_text"])
