from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_comment_node(args: SyntaxGraphArgs, comment: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        comment=comment,
        label_type="Comment",
    )
    return args.n_id
