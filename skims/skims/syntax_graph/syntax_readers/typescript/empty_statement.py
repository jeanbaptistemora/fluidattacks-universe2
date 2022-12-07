from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value_type="empty",
        label_type="Literal",
    )

    return args.n_id
