from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_object_creation_node(
    args: SyntaxGraphArgs, name: str, arguments_id: Optional[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        label_type="ObjectCreation",
    )

    if arguments_id:
        args.syntax_graph.nodes[args.n_id]["arguments_id"] = arguments_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(arguments_id)),
            label_ast="AST",
        )

    return args.n_id
