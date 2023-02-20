from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_variable_declaration_node(
    args: SyntaxGraphArgs,
    variable: str | None,
    variable_type: str | None,
    value_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="VariableDeclaration",
    )

    if variable_type:
        args.syntax_graph.nodes[args.n_id]["variable_type"] = variable_type
    if variable:
        args.syntax_graph.nodes[args.n_id]["variable"] = variable

    if value_id:
        args.syntax_graph.nodes[args.n_id]["value_id"] = value_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value_id)),
            label_ast="AST",
        )

    return args.n_id
