from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_variable_declarator_node(
    args: SyntaxGraphArgs,
    variable_name: str,
    value_id: Optional[NId],
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        variable_name=variable_name,
        label_type="VariableDeclarator",
    )
    if value_id:
        args.syntax_graph.nodes[args.n_id]["value_id"] = value_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value_id)),
            label_ast="AST",
        )

    return args.n_id
