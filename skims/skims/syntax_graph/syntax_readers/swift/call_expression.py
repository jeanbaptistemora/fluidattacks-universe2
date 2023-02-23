from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.call_expression import (
    build_call_expression,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
import utils.graph as g
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    expr_id = g.adj_ast(graph, args.n_id)[0]
    expr = node_to_str(graph, expr_id)

    suffix_id = g.match_ast_group_d(
        args.ast_graph, args.n_id, "value_argument", depth=3
    )
    args_id = None
    if suffix_id:
        args_id = [
            graph.nodes[suff].get("label_field_value") for suff in suffix_id
        ]
    return build_call_expression(args, expr, expr_id, args_id, None)
