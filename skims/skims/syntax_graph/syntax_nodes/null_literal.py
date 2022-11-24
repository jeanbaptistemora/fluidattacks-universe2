from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_null_literal_node(args: SyntaxGraphArgs, value: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        value_type="null",
        label_type="Literal",
    )

    return args.n_id
