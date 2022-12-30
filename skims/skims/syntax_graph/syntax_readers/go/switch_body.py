from itertools import (
    chain,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
    pred_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    ignored_labels = {
        "\n",
        "\r\n",
        "case",
        ":",
        "default",
    }
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchBody",
    )
    parent = pred_ast(graph, args.n_id)[0]
    expression_cases = match_ast_group_d(graph, parent, "expression_case")
    type_cases = match_ast_group_d(graph, parent, "type_case")
    default_case = match_ast_group_d(graph, parent, "default_case")

    for case_id in list(chain(type_cases, expression_cases, default_case)):
        value_id = None
        if val_id := graph.nodes[case_id].get("label_field_value") or (
            val_id := graph.nodes[case_id].get("label_field_type")
        ):
            value_id = val_id
            case_expr = node_to_str(graph, val_id)
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
        execution_ids = adj_ast(graph, case_id)

        filtered_ids = (
            _id
            for _id in execution_ids
            if args.ast_graph.nodes[_id]["label_type"] not in ignored_labels
            and _id != value_id
        )

        for statement_id in filtered_ids:
            args.syntax_graph.add_edge(
                case_id,
                args.generic(args.fork_n_id(statement_id)),
                label_ast="AST",
            )

    return args.n_id
