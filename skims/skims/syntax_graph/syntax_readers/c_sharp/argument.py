from model.graph_model import (
    NId,
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


def reader(args: SyntaxGraphArgs) -> NId:
    first_child, *other_childs = adj_ast(args.ast_graph, args.n_id)

    if not other_childs:
        return args.generic(args.fork_n_id(first_child))

    match = match_ast(args.ast_graph, args.n_id, "name_colon")
    if name_colon := match["name_colon"]:
        var_id = match_ast_d(args.ast_graph, name_colon, "identifier")
        return build_named_argument_node(args, var_id, val_id=match["__0__"])

    raise MissingCaseHandling(f"Bad argument handling in {args.n_id}")
