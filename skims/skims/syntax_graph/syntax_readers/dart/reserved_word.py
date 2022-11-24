from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.reserved_word import (
    build_reserved_word_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    return build_reserved_word_node(
        args, node_to_str(args.ast_graph, args.n_id)
    )
