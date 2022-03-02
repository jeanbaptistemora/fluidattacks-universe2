from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_this_expression_node(
    args: SyntaxGraphArgs,
    expression: Optional[str],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_id=expression,
        label_type="ThisExpression",
    )
    if expression:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(expression)),
            label_ast="AST",
        )

    return args.n_id
