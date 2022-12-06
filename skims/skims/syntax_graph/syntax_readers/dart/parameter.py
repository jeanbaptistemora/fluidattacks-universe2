from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    param_identifier = match_ast_d(graph, args.n_id, "identifier")
    param_name = None
    if param_identifier:
        param_name = node_to_str(graph, param_identifier)
    type_id = match_ast_d(graph, args.n_id, "type_arguments")
    var_id = match_ast_d(graph, args.n_id, "type_identifier")
    param_var = None
    if var_id:
        param_var = node_to_str(graph, var_id)

    c_ids = adj_ast(graph, args.n_id)
    invalid_childs = {"this", ".", "?", ";", "="}
    invalid_nodes = {param_identifier, type_id, var_id}
    return build_parameter_node(
        args,
        param_name,
        param_var,
        None,
        c_ids=(
            _id
            for _id in c_ids
            if _id not in invalid_nodes
            and graph.nodes[_id]["label_type"] not in invalid_childs
        ),
    )
