from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.lambda_expression import (
    build_lambda_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "inferred_parameters",
        "block",
    )
    parameters = match_childs.get("inferred_parameters")
    block_node = match_childs.get("block")
    return build_lambda_expression_node(
        args, None, parameters, block_node, None
    )
