from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_literal_node(
    args: SyntaxGraphArgs, value: str, var_type: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        value_type=var_type,
        label_type="Literal",
    )

    return args.n_id
