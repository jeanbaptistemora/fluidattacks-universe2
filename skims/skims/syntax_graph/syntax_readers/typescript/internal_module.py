from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(args.ast_graph, args.n_id, "namespace")
    var_name = node_to_str(args.ast_graph, str(match_childs["__0__"]))
    return build_variable_declaration_node(args, var_name, None, None)
