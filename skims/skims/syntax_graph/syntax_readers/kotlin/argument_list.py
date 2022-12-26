from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.argument_list import (
    build_argument_list_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = match_ast_group_d(graph, args.n_id, "value_argument")
    arg_ids = []
    for _id in c_ids:
        val_id = graph.nodes[_id].get("label_field_expression")
        if val_id:
            arg_ids.append(val_id)
    return build_argument_list_node(args, cast(Iterator[NId], arg_ids))
