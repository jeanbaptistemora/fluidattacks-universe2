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
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    var_id = as_attrs["label_field_left"]
    val_id = as_attrs["label_field_right"]

    op_id = match_ast_d(args.ast_graph, args.n_id, "assignment_operator")

    if not op_id:
        raise MissingCaseHandling(f"Bad assignment operator in {args.n_id}")

    operation = args.ast_graph.nodes[op_id]["label_text"]
    return build_assignment_node(args, var_id, val_id, operation)
