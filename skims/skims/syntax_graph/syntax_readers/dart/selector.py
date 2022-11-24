from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.selector import (
    build_selector_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    id_name = match_ast_d(
        graph, args.n_id, "unconditional_assignable_selector"
    ) or match_ast_d(graph, args.n_id, "conditional_assignable_selector")
    selector_name = None
    al_id = None
    if id_name:
        child_id = match_ast_d(graph, id_name, "identifier")
        if child_id:
            selector_name = node_to_str(graph, child_id)

    arg_id = match_ast_d(graph, args.n_id, "argument_part")
    if arg_id and (al_id := match_ast_d(graph, arg_id, "arguments")):
        return args.generic(args.fork_n_id(al_id))

    return build_selector_node(args, selector_name, None)
