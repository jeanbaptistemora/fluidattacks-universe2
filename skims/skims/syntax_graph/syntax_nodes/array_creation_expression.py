from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_array_creation_expression_node(
    args: SyntaxGraphArgs,
    arr_type: str,
    initializer_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        array_type=arr_type,
        label_type="ArrayCreation",
    )

    if initializer_id:
        args.syntax_graph.nodes[args.n_id]["initializer_id"] = initializer_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(initializer_id)),
            label_ast="AST",
        )

    return args.n_id
