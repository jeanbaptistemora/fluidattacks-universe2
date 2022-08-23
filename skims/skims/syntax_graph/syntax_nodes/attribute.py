from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_attribute_node(
    args: SyntaxGraphArgs,
    attr_name: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=attr_name,
        label_type="Attribute",
    )

    return args.n_id
