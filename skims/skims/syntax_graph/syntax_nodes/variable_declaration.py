from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_variable_declaration_node(
    args: SyntaxGraphArgs, variable: str, variable_type: str, value_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        variable=variable,
        variable_type=variable_type,
        value_id=value_id,
        label_type="VariableDeclaration",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(value_id)),
        label_ast="AST",
    )

    return args.n_id
