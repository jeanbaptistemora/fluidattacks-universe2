from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    text_node = n_attrs["label_field_text"]
    label_text = args.ast_graph.nodes[text_node]
    return build_string_literal_node(args, label_text["label_text"])
