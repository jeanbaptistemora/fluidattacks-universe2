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
    n_attrs = args.ast_graph.nodes[args.n_id]
    val_id = n_attrs["label_field_value"]
    match_childs = match_ast(args.ast_graph, args.n_id, "=")
    var_name = node_to_str(args.ast_graph, str(match_childs["__0__"]))
    return build_variable_declaration_node(args, var_name, None, val_id)
