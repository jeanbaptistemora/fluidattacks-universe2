from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.prefix_operation import (
    build_prefix_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)

    if len(c_ids) == 2:
        prefix_id, expression_id = c_ids
        prefix = node_to_str(args.ast_graph, prefix_id)
        return build_prefix_node(args, prefix, expression_id)

    raise MissingCaseHandling(f"Bad prefix expression handling in {args.n_id}")
