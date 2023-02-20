from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_lambda_expression_node(
    args: SyntaxGraphArgs,
    var_name: str,
    block_id: NId,
    parameters_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="LambdaExpression",
        identifier=var_name,
        block_id=block_id,
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    if parameters_id:
        args.syntax_graph.nodes[args.n_id]["parameters_id"] = parameters_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters_id)),
            label_ast="AST",
        )

    return args.n_id
