from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_lambda_expression_node(
    args: SyntaxGraphArgs,
    var_name: Optional[str],
    parameters: Optional[str],
    block_id: Optional[str],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block_id,
        label_type="LambdaExpression",
    )

    if var_name:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(var_name)),
            label_ast="AST",
        )

    if parameters:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters)),
            label_ast="AST",
        )

    if block_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_id)),
            label_ast="AST",
        )

    return args.n_id
