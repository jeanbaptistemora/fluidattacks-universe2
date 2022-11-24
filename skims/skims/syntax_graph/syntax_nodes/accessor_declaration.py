from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_accessor_declaration_node(
    args: SyntaxGraphArgs, var_type: str, block: Optional[str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        var_type=var_type,
        label_type="AccessorDeclaration",
    )
    if block:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block)),
            label_ast="AST",
        )

    return args.n_id
