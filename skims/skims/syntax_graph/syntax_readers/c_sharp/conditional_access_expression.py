from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.conditional_access_expression import (
    build_conditional_access_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    condition = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    binding = g.match_ast_d(
        args.ast_graph, args.n_id, "member_binding_expression"
    )
    if not binding:
        binding = g.match_ast_d(
            args.ast_graph, args.n_id, "element_binding_expression"
        )
    return build_conditional_access_expression_node(args, condition, binding)
