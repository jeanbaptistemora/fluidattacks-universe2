from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Any,
    Optional,
)


def build_method_declaration_node(
    args: SyntaxGraphArgs,
    name: str,
    block_id: Any,
    parameters_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        label_type="MethodDeclaration",
    )

    if parameters_id:
        args.syntax_graph.nodes[args.n_id]["parameters_id"] = parameters_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters_id)),
            label_ast="AST",
        )

    if block_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_id)),
            label_ast="AST",
        )

    return args.n_id
