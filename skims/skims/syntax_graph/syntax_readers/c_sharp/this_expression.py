from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.this_expression import (
    build_this_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    pred = g.pred_ast(args.ast_graph, args.n_id)
    match = g.match_ast(args.ast_graph, pred[0], "identifier")
    expression = match["identifier"] if "identifier" in match else None
    return build_this_expression_node(args, expression)
