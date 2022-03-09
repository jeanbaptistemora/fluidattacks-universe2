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
    match_childs = match_ast(args.ast_graph, args.n_id)
    var_name = args.ast_graph.nodes[match_childs["__0__"]]["label_text"]
    expression_node = match_childs["__2__"]
    return build_lambda_expression_node(args, var_name, expression_node)
