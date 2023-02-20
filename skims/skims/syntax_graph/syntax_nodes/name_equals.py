from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_name_equals_node(
    args: SyntaxGraphArgs,
    name_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name_id=name_id,
        label_type="NameEquals",
    )

    if name_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(name_id)),
            label_ast="AST",
        )

    return args.n_id
