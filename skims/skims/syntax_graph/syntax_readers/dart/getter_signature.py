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
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    var_id = graph.nodes[args.n_id]["label_field_name"]
    var_name = node_to_str(graph, var_id)
    var_type = match_ast_d(graph, args.n_id, "type_identifier")

    return build_variable_declaration_node(args, var_name, var_type, var_id)
