from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.field_declaration import (
    build_field_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_var = g.match_ast(args.ast_graph, args.n_id, "variable_declaration")
    var = match_var["variable_declaration"]
    return build_field_declaration_node(args, var)
