from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    definition_id = match_ast_d(
        graph, args.n_id, "initialized_variable_definition"
    )
    if not definition_id:
        raise MissingCaseHandling(f"Bad variable definition in {args.n_id}")

    var_type = (
        fr_child
        if (fr_child := match_ast(graph, args.n_id).get("__0__"))
        and graph.nodes[fr_child]["label_type"] == "type_identifier"
        else None
    )

    var_id = graph.nodes[definition_id]["label_field_name"]
    var_name = node_to_str(graph, var_id)

    value_id = graph.nodes[definition_id].get("label_field_value")

    return build_variable_declaration_node(args, var_name, var_type, value_id)
