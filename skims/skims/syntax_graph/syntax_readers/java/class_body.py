from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_body import (
    build_class_body_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    _, *c_ids, _ = adj_ast(graph, args.n_id)  # do not consider { }
    forked_ids = []
    for _id in c_ids:
        if graph.nodes[_id]["label_type"] == "field_declaration":
            forked_ids += match_ast_group_d(graph, _id, "variable_declarator")
        else:
            forked_ids.append(_id)

    return build_class_body_node(args, forked_ids)
