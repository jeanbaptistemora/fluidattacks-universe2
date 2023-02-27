from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    literal_text = n_attrs.get("label_text")
    if not literal_text:
        literal_text = node_to_str(args.ast_graph, args.n_id)
    return build_string_literal_node(args, literal_text)
