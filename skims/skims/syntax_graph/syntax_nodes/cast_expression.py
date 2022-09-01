from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_cast_expression_node(
    args: SyntaxGraphArgs,
    type_id: NId,
    val_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable_id=type_id,
        value_id=val_id,
        label_type="CastExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(type_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(val_id)),
        label_ast="AST",
    )

    return args.n_id
