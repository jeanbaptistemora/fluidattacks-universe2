from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_dimensions_expr_node(
    args: SyntaxGraphArgs, expr_type: str | None
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value_id=expr_type,
        label_type="DimensionsExpr",
    )

    if expr_type:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(expr_type)),
            label_ast="AST",
        )

    return args.n_id
