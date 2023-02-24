from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    C_SHARP_EXPRESSION,
)
from syntax_graph.syntax_nodes.argument import (
    build_argument_node,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    first_child, *other_childs = adj_ast(graph, args.n_id)

    if not other_childs:
        return args.generic(args.fork_n_id(first_child))

    match = match_ast(graph, args.n_id, "name_colon")
    if (
        (name_colon := match.get("name_colon"))
        and (var_id := match_ast_d(graph, name_colon, "identifier"))
        and (val_id := match.get("__0__"))
    ):
        arg_name = node_to_str(graph, var_id)
        return build_named_argument_node(args, arg_name, val_id)

    if valid_childs := [
        _id
        for _id in adj_ast(graph, args.n_id)
        if graph.nodes[_id]["label_type"]
        in C_SHARP_EXPRESSION.union({"declaration_expression"})
    ]:
        return build_argument_node(args, iter(valid_childs))

    raise MissingCaseHandling(f"Bad argument handling in {args.n_id}")
