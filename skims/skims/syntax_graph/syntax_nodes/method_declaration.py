from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_method_declaration_node(
    args: SyntaxGraphArgs, name: str, block_id: str, parameters_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        parameters_id=parameters_id,
        label_type="MethodDeclaration",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(parameters_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    return args.n_id
