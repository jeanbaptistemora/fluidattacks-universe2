from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_reserved_word_node(args: SyntaxGraphArgs, value: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        label_type="ReservedWord",
    )

    return args.n_id
