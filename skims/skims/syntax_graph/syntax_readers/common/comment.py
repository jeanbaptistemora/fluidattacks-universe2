from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.comment import (
    build_comment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    comment = args.ast_graph.nodes[args.n_id]["label_text"]
    return build_comment_node(args, comment)
