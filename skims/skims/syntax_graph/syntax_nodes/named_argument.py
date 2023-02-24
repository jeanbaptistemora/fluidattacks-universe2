from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_named_argument_node(
    args: SyntaxGraphArgs,
    arg_name: str | None,
    val_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value_id=val_id,
        label_type="NamedArgument",
    )

    if arg_name:
        args.syntax_graph.nodes[args.n_id]["argument_name"] = arg_name

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(val_id)),
        label_ast="AST",
    )

    return args.n_id
