from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    alias_id = graph.nodes[args.n_id]["label_field_alias"]
    var_id = adj_ast(graph, alias_id)[0]
    val_id = adj_ast(graph, args.n_id)[0]
    return build_assignment_node(args, var_id, val_id, None)
