from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    get_ast_childs,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(args.ast_graph, args.n_id)
    ignored_types = {";", "(", ")", "super", "comment"}
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_types
    ]
    if (
        (sel := get_ast_childs(graph, args.n_id, label_type="selector"))
        and len(sel) == 2
        and (
            child_s1 := match_ast_d(
                graph, sel[0], "unconditional_assignable_selector"
            )
        )
        and (child_s2 := match_ast_d(graph, sel[1], "argument_part"))
    ):
        expr_id = adj_ast(graph, child_s1)[1]
        expr = (
            node_to_str(graph, filtered_ids[0])
            + "."
            + node_to_str(graph, expr_id)
        )
        args_id = match_ast_d(graph, child_s2, "arguments")
        return build_method_invocation_node(
            args, expr, expr_id, args_id, filtered_ids[0]
        )

    return build_expression_statement_node(args, iter(filtered_ids))
