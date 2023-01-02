from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.return_statment import (
    build_return_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = match_ast(graph, args.n_id, "return")
    if len(childs) == 2 and (stmt_id := childs["__0__"]):
        if (
            graph.nodes[stmt_id]["label_type"] == "expression_list"
            and (expr_childs := adj_ast(graph, stmt_id))
            and len(expr_childs) == 1
        ):
            return build_return_node(args, expr_childs[0])

        return build_return_node(args, stmt_id)

    return build_return_node(args, None)
