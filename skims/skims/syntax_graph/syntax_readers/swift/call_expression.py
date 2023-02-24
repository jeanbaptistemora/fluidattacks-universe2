from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
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

    suffix_id = g.match_ast_d(
        args.ast_graph, args.n_id, "value_arguments", depth=2
    )

    return build_method_invocation_node(args, expr, expr_id, suffix_id, None)
