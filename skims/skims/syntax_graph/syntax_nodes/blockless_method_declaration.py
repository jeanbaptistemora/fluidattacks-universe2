from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_blockless_method_declaration_node(
    args: SyntaxGraphArgs,
    name: Optional[NId],
    parameters_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="BlocklessMethodDeclaration",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    if parameters_id:
        args.syntax_graph.nodes[args.n_id]["parameters_id"] = parameters_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters_id)),
            label_ast="AST",
        )

    return args.n_id
