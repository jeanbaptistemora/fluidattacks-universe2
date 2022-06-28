from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declarator import (
    build_variable_declarator_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    ident_id = str(args.ast_graph.nodes[args.n_id]["label_field_name"])
    return build_variable_declarator_node(args, ident_id)
