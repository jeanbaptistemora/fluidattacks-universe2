from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    C_SHARP_EXPRESSION,
    C_SHARP_STATEMENT,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(args.ast_graph, args.n_id)
    body_id = [
        _id
        for _id in c_ids
        if graph.nodes[_id]["label_type"] in C_SHARP_STATEMENT
    ].pop()
    if graph.nodes[body_id]["label_type"] == "expression_statement":
        body_id = adj_ast(graph, body_id)[0]

    condition_node = [
        _id
        for _id in c_ids
        if graph.nodes[_id]["label_type"] in C_SHARP_EXPRESSION
    ].pop()

    return build_do_statement_node(args, body_id, condition_node)
