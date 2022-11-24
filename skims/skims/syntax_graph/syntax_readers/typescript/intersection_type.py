from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.new_expression import (
    build_new_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(args.ast_graph, args.n_id, "&")
    const_id = str(match_childs["__0__"])
    args_id = match_childs.get("__1__")
    return build_new_expression_node(args, const_id, args_id)
