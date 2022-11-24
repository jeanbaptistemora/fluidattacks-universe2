from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.element_binding_expression import (
    build_element_binding_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs_match = list(g.match_ast(args.ast_graph, args.n_id).values())
    childs = list(filter(None, childs_match))
    return build_element_binding_expression_node(args, childs)
