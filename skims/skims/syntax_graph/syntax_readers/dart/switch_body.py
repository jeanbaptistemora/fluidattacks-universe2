from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchBody",
    )
    label_ids = match_ast_group_d(graph, args.n_id, "switch_label")
    case_ids = match_ast_group_d(graph, args.n_id, "block")

    for label_id, case_id in zip(label_ids, case_ids):
        label_identifier = match_ast(graph, label_id, ":", "case_builtin").get(
            "__0__"
        )
        if label_identifier:
            case_expr = node_to_str(graph, label_identifier)
        else:
            case_expr = "Default"

        args.syntax_graph.add_node(
            case_id,
            case_expression=case_expr,
            label_type="SwitchSection",
        )

        args.syntax_graph.add_edge(
            args.n_id,
            case_id,
            label_ast="AST",
        )
        _, *execution_ids, _ = adj_ast(graph, case_id)

        for statement_id in execution_ids:
            args.syntax_graph.add_edge(
                case_id,
                args.generic(args.fork_n_id(statement_id)),
                label_ast="AST",
            )

    return args.n_id
