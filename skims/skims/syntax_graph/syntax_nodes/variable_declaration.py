from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_variable_declaration_node(
    args: SyntaxGraphArgs,
    variable: str,
    variable_type: str,
    value_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable=variable,
        variable_type=variable_type,
        label_type="VariableDeclaration",
    )

    if value_id:
        args.syntax_graph.nodes[args.n_id]["value_id"] = value_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value_id)),
            label_ast="AST",
        )

    return args.n_id
