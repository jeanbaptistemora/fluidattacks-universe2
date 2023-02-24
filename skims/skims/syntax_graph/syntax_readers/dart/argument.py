from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    DART_PRIMARY_TYPES,
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

    if other_childs and (label_id := match_ast_d(graph, args.n_id, "label")):
        var_id = adj_ast(graph, label_id)[0]
        arg_name = node_to_str(graph, var_id)
        return build_named_argument_node(args, arg_name, other_childs[0])

    if valid_childs := [
        _id
        for _id in adj_ast(args.ast_graph, args.n_id)
        if args.ast_graph.nodes[_id]["label_type"] in DART_PRIMARY_TYPES
    ]:
        return build_argument_node(args, iter(valid_childs))

    raise MissingCaseHandling(f"Bad argument handling in {args.n_id}")
