from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    children = adj_ast(graph, args.n_id)
    if len(children) < 3:
        raise MissingCaseHandling(f"Bad assignment in {args.n_id}")

    var_id = children[0]
    val_id = children[2]
    return build_assignment_node(args, var_id, val_id, None)
