from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_body import (
    build_switch_body_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    case_ids = match_ast_group_d(graph, args.n_id, "when_entry")
    return build_switch_body_node(args, case_ids, None)
