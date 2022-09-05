from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.update_expression import (
    build_update_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = match_ast(args.ast_graph, args.n_id)
    exp_type = str(args.ast_graph.nodes[c_ids["__1__"]]["label_text"])
    ident_id = str(c_ids["__0__"])

    return build_update_expression_node(args, exp_type, ident_id)
