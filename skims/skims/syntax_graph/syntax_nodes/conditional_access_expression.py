from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_conditional_access_expression_node(
    args: SyntaxGraphArgs,
    condition: str,
    binding: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        condition=condition,
        label_type="ConditionalAccessExpression",
    )

    if binding:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(binding)),
            label_ast="AST",
        )

    return args.n_id
