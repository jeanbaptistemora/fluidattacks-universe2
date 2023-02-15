from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = adj_ast(
        args.ast_graph,
        args.n_id,
    )
    invalid_types = {
        "assert",
        ",",
        ")",
        "(",
    }

    valid_childs = [
        _id
        for _id in childs
        if args.ast_graph.nodes[_id]["label_type"] not in invalid_types
    ]

    return build_expression_statement_node(args, iter(valid_childs))
