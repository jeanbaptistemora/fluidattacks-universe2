from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_statement import (
    build_switch_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    body_id = match_ast_d(graph, args.n_id, "switch")
    value_id = graph.nodes[args.n_id]["label_field_value"]
    return build_switch_statement_node(args, str(body_id), value_id)
