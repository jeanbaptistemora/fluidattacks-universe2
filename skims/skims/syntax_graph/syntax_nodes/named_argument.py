from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_named_argument_node(
    args: SyntaxGraphArgs, var_id: NId, val_id: NId
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable_id=var_id,
        value_id=val_id,
        label_type="NamedArgument",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(val_id)),
        label_ast="AST",
    )

    return args.n_id
