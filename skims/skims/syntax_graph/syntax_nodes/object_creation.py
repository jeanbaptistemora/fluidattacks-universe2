from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_object_creation_node(
    args: SyntaxGraphArgs, name: str, arguments_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        arguments_id=arguments_id,
        danger=False,
        evaluated=False,
        label_type="ObjectCreation",
    )

    if arguments_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(arguments_id)),
            label_ast="AST",
        )

    return args.n_id
