from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_attribute_node(
    args: SyntaxGraphArgs,
    attr_name: str,
    attr_list: str | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=attr_name,
        label_type="Attribute",
    )

    if attr_list:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(attr_list)),
            label_ast="AST",
        )

    return args.n_id
