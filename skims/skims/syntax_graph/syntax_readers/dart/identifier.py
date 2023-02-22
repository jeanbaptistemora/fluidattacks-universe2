from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
)
from syntax_graph.syntax_nodes.symbol_lookup import (
    build_symbol_lookup_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    get_ast_childs,
    match_ast_d,
    pred,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    symbol = graph.nodes[args.n_id]["label_text"]
    pred_nid = pred(graph, args.n_id)[0]

    if (
        graph.nodes[pred_nid]["label_type"]
        in {"initialized_variable_definition", "assignment_expression"}
        and (sel := get_ast_childs(graph, pred_nid, label_type="selector"))
        and len(sel) == 2
        and (
            child_s1 := match_ast_d(
                graph, sel[0], "unconditional_assignable_selector"
            )
        )
        and (child_s2 := match_ast_d(graph, sel[1], "argument_part"))
    ):
        expr_id = adj_ast(graph, child_s1)[1]
        expr = symbol + "." + node_to_str(graph, expr_id)
        args_id = match_ast_d(graph, child_s2, "arguments")
        return build_method_invocation_node(args, expr, expr_id, args_id, None)
    if (
        graph.nodes[pred_nid]["label_type"] == "static_final_declaration"
        and (sel := get_ast_childs(graph, pred_nid, label_type="selector"))
        and len(sel) == 1
        and (child_args := match_ast_d(graph, sel[0], "argument_part"))
    ):
        args_id = match_ast_d(graph, child_args, "arguments")
        return build_method_invocation_node(args, symbol, None, args_id, None)

    return build_symbol_lookup_node(args, symbol)
