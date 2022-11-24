from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_operator_node(args: SyntaxGraphArgs, value: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        label_type="Operator",
    )

    return args.n_id
