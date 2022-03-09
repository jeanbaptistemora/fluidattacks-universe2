from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_lambda_expression_node(
    args: SyntaxGraphArgs, var_name: str, expression_node: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable=var_name,
        label_type="LambdaExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression_node)),
        label_ast="AST",
    )

    return args.n_id
